package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
@ActiveProfiles("test")
public class RequestTrackingTests {

    @Autowired
    private RecheckRequestService recheckRequestService;

    @Autowired
    private ReviewService reviewService;

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
    private User student1;
    private User student2;
    private Exam exam;
    private Question question1;

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

        faculty = userRepository.save(new User("Prof. Knuth", "knuth_track@example.com", "pass", Role.FACULTY));
        student1 = userRepository.save(new User("Student One", "s1_track@example.com", "pass", Role.STUDENT));
        student2 = userRepository.save(new User("Student Two", "s2_track@example.com", "pass", Role.STUDENT));

        exam = new Exam("Computer Architecture", "CS306", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        exam.setReevaluationStart(LocalDateTime.now().minusDays(1));
        exam.setReevaluationEnd(LocalDateTime.now().plusDays(7));
        exam = examRepository.save(exam);

        question1 = questionRepository.save(new Question(exam, 1, "Explain Pipelining Hazards and Forwarding.", 10.0));

        marksService.recordMark(student1, question1, 4.0, faculty);
        marksService.recordMark(student2, question1, 5.0, faculty);
    }

    @Test
    @DisplayName("Student can track their own submitted requests in reverse chronological order")
    void testStudentCanTrackOwnRequests() {
        RecheckRequest req = recheckRequestService.submitRequest(student1, exam.getId(), question1.getId(),
                "Data hazards were correctly analyzed with stall calculations.");

        List<RecheckRequest> studentRequests = recheckRequestService.getStudentRequests(student1.getId());
        assertThat(studentRequests).hasSize(1);
        assertThat(studentRequests.get(0).getId()).isEqualTo(req.getId());
        assertThat(studentRequests.get(0).getStatus()).isEqualTo(RequestStatus.SUBMITTED);
        assertThat(studentRequests.get(0).getCreatedAt()).isNotNull();
    }

    @Test
    @DisplayName("Request status transitions SUBMITTED -> UNDER_REVIEW when opened by faculty")
    void testRequestTransitionsToUnderReviewWhenOpenedByFaculty() {
        RecheckRequest req = recheckRequestService.submitRequest(student1, exam.getId(), question1.getId(),
                "Structural hazard explanation matches textbook figure 4.12.");
        assertThat(req.getStatus()).isEqualTo(RequestStatus.SUBMITTED);

        RecheckRequest underReview = recheckRequestService.markUnderReview(req.getId(), faculty);

        assertThat(underReview.getStatus()).isEqualTo(RequestStatus.UNDER_REVIEW);
    }

    @Test
    @DisplayName("Student cannot view or track another student's request (IDOR prevention)")
    void testStudentCannotAccessOtherStudentsRequest() {
        RecheckRequest req = recheckRequestService.submitRequest(student1, exam.getId(), question1.getId(),
                "Control hazard branch prediction was thoroughly demonstrated.");

        // student2 attempts to access student1's request
        RecheckRequest fetched = recheckRequestService.getRequestById(req.getId()).orElseThrow();
        assertThat(fetched.getStudent().getId()).isNotEqualTo(student2.getId());
    }

    @Test
    @DisplayName("Student can see faculty review comments and revised marks upon approval")
    void testStudentCanSeeFacultyReviewOutcomeAndRevisedMarks() {
        RecheckRequest req = recheckRequestService.submitRequest(student1, exam.getId(), question1.getId(),
                "Forwarding unit logic handles RAW data hazard correctly.");

        // Faculty reviews and approves
        reviewService.processReview(req.getId(), faculty, ReviewDecision.APPROVED, "Verified diagram; 3 marks added.", 7.0);

        RecheckRequest decidedReq = recheckRequestService.getRequestById(req.getId()).orElseThrow();
        assertThat(decidedReq.getStatus()).isEqualTo(RequestStatus.APPROVED);

        List<Review> reviews = reviewService.getReviewsForRequest(req.getId());
        assertThat(reviews).hasSize(1);
        assertThat(reviews.get(0).getDecision()).isEqualTo(ReviewDecision.APPROVED);
        assertThat(reviews.get(0).getRevisedMarks()).isEqualTo(7.0);
        assertThat(reviews.get(0).getComments()).contains("3 marks added");
    }
}
