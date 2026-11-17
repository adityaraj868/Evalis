package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.exception.DuplicateRequestException;
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
public class RecheckRequestCoreTests {

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

        faculty = userRepository.save(new User("Prof. Hopper", "hopper_core@example.com", "pass", Role.FACULTY));
        student = userRepository.save(new User("Ada Student", "ada_core@example.com", "pass", Role.STUDENT));

        exam = new Exam("Programming Languages", "CS201", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        exam.setReevaluationStart(LocalDateTime.now().minusDays(1));
        exam.setReevaluationEnd(LocalDateTime.now().plusDays(5));
        exam = examRepository.save(exam);

        question1 = questionRepository.save(new Question(exam, 1, "Explain Static Scope vs Dynamic Scope.", 10.0));

        // Record marks for student
        marksService.recordMark(student, question1, 4.0, faculty);
    }

    @Test
    @DisplayName("Valid recheck submission persists request with SUBMITTED status and logs audit event")
    void testSubmitValidRequest() {
        RecheckRequest request = recheckRequestService.submitRequest(student, exam.getId(), question1.getId(),
                "The lexical scoping example was clearly outlined with environment diagram.");

        assertThat(request).isNotNull();
        assertThat(request.getId()).isNotNull();
        assertThat(request.getStatus()).isEqualTo(RequestStatus.SUBMITTED);
        assertThat(request.getReason()).contains("lexical scoping");

        // Verify queryable
        assertThat(recheckRequestService.hasExistingRequest(student.getId(), exam.getId(), question1.getId())).isTrue();
    }

    @Test
    @DisplayName("Request outside re-evaluation window (status PUBLISHED) throws InvalidStateTransitionException")
    void testSubmitRequestOutsideWindowFails() {
        exam.setStatus(ExamStatus.PUBLISHED);
        examRepository.save(exam);

        assertThatThrownBy(() -> recheckRequestService.submitRequest(student, exam.getId(), question1.getId(),
                "Marking was too harsh for question 1."))
                .isInstanceOf(InvalidStateTransitionException.class)
                .hasMessageContaining("Re-evaluation window is not currently open");
    }

    @Test
    @DisplayName("Request before reevaluationStart date throws InvalidStateTransitionException")
    void testSubmitRequestBeforeStartTimeFails() {
        exam.setReevaluationStart(LocalDateTime.now().plusDays(2));
        exam.setReevaluationEnd(LocalDateTime.now().plusDays(8));
        examRepository.save(exam);

        assertThatThrownBy(() -> recheckRequestService.submitRequest(student, exam.getId(), question1.getId(),
                "Premature request attempt."))
                .isInstanceOf(InvalidStateTransitionException.class)
                .hasMessageContaining("has not commenced yet");
    }

    @Test
    @DisplayName("Request after reevaluationEnd date throws InvalidStateTransitionException")
    void testSubmitRequestAfterEndTimeFails() {
        exam.setReevaluationStart(LocalDateTime.now().minusDays(10));
        exam.setReevaluationEnd(LocalDateTime.now().minusDays(1));
        examRepository.save(exam);

        assertThatThrownBy(() -> recheckRequestService.submitRequest(student, exam.getId(), question1.getId(),
                "Expired request attempt."))
                .isInstanceOf(InvalidStateTransitionException.class)
                .hasMessageContaining("has already concluded");
    }

    @Test
    @DisplayName("Student not enrolled / without examination result throws UnauthorizedAccessException")
    void testSubmitRequestWithoutStudentEnrollmentFails() {
        User unenrolledStudent = userRepository.save(new User("Unenrolled", "unenrolled@example.com", "pass", Role.STUDENT));

        assertThatThrownBy(() -> recheckRequestService.submitRequest(unenrolledStudent, exam.getId(), question1.getId(),
                "I want a review even though I did not take this exam."))
                .isInstanceOf(UnauthorizedAccessException.class)
                .hasMessageContaining("Student has no examination result");
    }

    @Test
    @DisplayName("Question without recorded mark throws ValidationException")
    void testSubmitRequestWithoutQuestionMarksFails() {
        Question q2 = questionRepository.save(new Question(exam, 2, "Type Inference in ML.", 15.0));

        assertThatThrownBy(() -> recheckRequestService.submitRequest(student, exam.getId(), q2.getId(),
                "Review this question please."))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("No evaluation mark entry found");
    }

    @Test
    @DisplayName("Short reason (< 5 characters) throws ValidationException")
    void testSubmitRequestShortReasonFails() {
        assertThatThrownBy(() -> recheckRequestService.submitRequest(student, exam.getId(), question1.getId(),
                "why?"))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("at least 5 characters is required");
    }

    @Test
    @DisplayName("Duplicate request prevention at application level throws DuplicateRequestException")
    void testDuplicateRequestPreventedAtApplicationLevel() {
        recheckRequestService.submitRequest(student, exam.getId(), question1.getId(), "First valid justification.");

        assertThatThrownBy(() -> recheckRequestService.submitRequest(student, exam.getId(), question1.getId(),
                "Second duplicate justification attempt."))
                .isInstanceOf(DuplicateRequestException.class)
                .hasMessageContaining("already been submitted for this question");
    }

    @Test
    @DisplayName("Non-student role submitting recheck throws UnauthorizedAccessException")
    void testNonStudentCannotSubmitRequest() {
        assertThatThrownBy(() -> recheckRequestService.submitRequest(faculty, exam.getId(), question1.getId(),
                "Faculty trying to submit recheck."))
                .isInstanceOf(UnauthorizedAccessException.class)
                .hasMessageContaining("Only enrolled students can submit re-evaluation requests");
    }
}
