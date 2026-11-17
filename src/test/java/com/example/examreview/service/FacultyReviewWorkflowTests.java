package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.exception.InvalidStateTransitionException;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.exception.ValidationException;
import com.example.examreview.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
@ActiveProfiles("test")
public class FacultyReviewWorkflowTests {

    @Autowired
    private ReviewService reviewService;

    @Autowired
    private RecheckRequestService recheckRequestService;

    @Autowired
    private MarksService marksService;

    @Autowired
    private ExamRepository examRepository;

    @Autowired
    private QuestionRepository questionRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private QuestionMarkRepository questionMarkRepository;

    @Autowired
    private StudentResultRepository studentResultRepository;

    @Autowired
    private RecheckRequestRepository recheckRequestRepository;

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private AuditLogRepository auditLogRepository;

    private User faculty;
    private User student;
    private Exam exam;
    private Question q1;
    private RecheckRequest request;

    @BeforeEach
    void setUp() {
        reviewRepository.deleteAll();
        recheckRequestRepository.deleteAll();
        questionMarkRepository.deleteAll();
        studentResultRepository.deleteAll();
        questionRepository.deleteAll();
        examRepository.deleteAll();
        auditLogRepository.deleteAll();
        userRepository.deleteAll();

        faculty = userRepository.save(new User("Prof. Shannon", "shannon_rev@example.com", "pass", Role.FACULTY));
        student = userRepository.save(new User("Claude Student", "claude_rev@example.com", "pass", Role.STUDENT));

        exam = new Exam("Information Theory", "CS405", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        exam.setReevaluationStart(LocalDateTime.now().minusDays(1));
        exam.setReevaluationEnd(LocalDateTime.now().plusDays(7));
        exam = examRepository.save(exam);

        q1 = questionRepository.save(new Question(exam, 1, "Compute entropy of source H(X).", 10.0));

        marksService.recordMark(student, q1, 3.0, faculty);

        request = recheckRequestService.submitRequest(student, exam.getId(), q1.getId(),
                "Entropy calculation used log base 2 correctly, please re-evaluate step 2.");
    }

    @Test
    @DisplayName("Approval workflow updates marks, recalculates total, sets APPROVED status, and logs audit")
    void testApproveRequestUpdatesMarksAndRecalculatesTotal() {
        Review review = reviewService.processReview(request.getId(), faculty, ReviewDecision.APPROVED,
                "Awarded 4 additional marks after verification of step 2.", 7.0);

        assertThat(review).isNotNull();
        assertThat(review.getDecision()).isEqualTo(ReviewDecision.APPROVED);
        assertThat(review.getRevisedMarks()).isEqualTo(7.0);

        RecheckRequest updatedReq = recheckRequestService.getRequestById(request.getId()).orElseThrow();
        assertThat(updatedReq.getStatus()).isEqualTo(RequestStatus.APPROVED);

        QuestionMark qm = marksService.getQuestionMark(student.getId(), q1.getId()).orElseThrow();
        assertThat(qm.getMarksObtained()).isEqualTo(7.0);

        StudentResult sr = marksService.getStudentResult(student.getId(), exam.getId()).orElseThrow();
        assertThat(sr.getTotalMarks()).isEqualTo(7.0);
    }

    @Test
    @DisplayName("Rejection workflow maintains original marks and sets REJECTED status")
    void testRejectRequestMaintainsOriginalMarks() {
        Review review = reviewService.processReview(request.getId(), faculty, ReviewDecision.REJECTED,
                "Log base 10 was mistakenly used in equation 3. Original evaluation maintained.", null);

        assertThat(review).isNotNull();
        assertThat(review.getDecision()).isEqualTo(ReviewDecision.REJECTED);

        RecheckRequest updatedReq = recheckRequestService.getRequestById(request.getId()).orElseThrow();
        assertThat(updatedReq.getStatus()).isEqualTo(RequestStatus.REJECTED);

        QuestionMark qm = marksService.getQuestionMark(student.getId(), q1.getId()).orElseThrow();
        assertThat(qm.getMarksObtained()).isEqualTo(3.0); // Unaltered

        StudentResult sr = marksService.getStudentResult(student.getId(), exam.getId()).orElseThrow();
        assertThat(sr.getTotalMarks()).isEqualTo(3.0); // Unaltered
    }

    @Test
    @DisplayName("Approval without revised marks throws ValidationException")
    void testApproveRequestWithMissingMarksFails() {
        assertThatThrownBy(() -> reviewService.processReview(request.getId(), faculty, ReviewDecision.APPROVED, "No marks provided", null))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("Revised marks must be provided when approving");
    }

    @Test
    @DisplayName("Approval with negative revised marks throws ValidationException")
    void testApproveRequestWithNegativeMarksFails() {
        assertThatThrownBy(() -> reviewService.processReview(request.getId(), faculty, ReviewDecision.APPROVED, "Negative marks", -1.0))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("Revised marks cannot be negative");
    }

    @Test
    @DisplayName("Approval with marks exceeding maximum question marks throws ValidationException")
    void testApproveRequestExceedingMaxMarksFails() {
        // q1 maxMarks is 10.0
        assertThatThrownBy(() -> reviewService.processReview(request.getId(), faculty, ReviewDecision.APPROVED, "Exceeds max", 12.0))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("cannot exceed maximum question marks");
    }

    @Test
    @DisplayName("Attempting to review an already decided request throws InvalidStateTransitionException")
    void testCannotReviewAlreadyDecidedRequest() {
        reviewService.processReview(request.getId(), faculty, ReviewDecision.REJECTED, "First decision", null);

        assertThatThrownBy(() -> reviewService.processReview(request.getId(), faculty, ReviewDecision.APPROVED, "Second attempt", 8.0))
                .isInstanceOf(InvalidStateTransitionException.class)
                .hasMessageContaining("already received a final decision");
    }

    @Test
    @DisplayName("Non-faculty user attempting to process a review throws UnauthorizedAccessException")
    void testNonFacultyCannotReviewRequest() {
        assertThatThrownBy(() -> reviewService.processReview(request.getId(), student, ReviewDecision.APPROVED, "Student approving own request", 10.0))
                .isInstanceOf(UnauthorizedAccessException.class)
                .hasMessageContaining("Only faculty members or administrators can review");
    }
}
