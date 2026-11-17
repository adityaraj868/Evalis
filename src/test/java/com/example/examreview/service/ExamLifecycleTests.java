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
import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
@ActiveProfiles("test")
public class ExamLifecycleTests {

    @Autowired
    private ExamService examService;

    @Autowired
    private ExamRepository examRepository;

    @Autowired
    private QuestionRepository questionRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RecheckRequestRepository recheckRequestRepository;

    @Autowired
    private StudentResultRepository studentResultRepository;

    @Autowired
    private QuestionMarkRepository questionMarkRepository;

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private AuditLogRepository auditLogRepository;

    private User faculty;
    private User student;

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

        faculty = userRepository.save(new User("Prof. Dijkstra", "dijkstra_test@example.com", "hash", Role.FACULTY));
        student = userRepository.save(new User("Alan Student", "alan_test@example.com", "hash", Role.STUDENT));
    }

    @Test
    @DisplayName("Create exam in DRAFT status with initial questions")
    void testCreateExamWithQuestions() {
        Exam exam = new Exam("Compiler Design", "CS401", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.DRAFT);

        List<Question> questions = new ArrayList<>();
        questions.add(new Question(exam, 1, "Construct LL(1) parsing table.", 15.0));
        questions.add(new Question(exam, 2, "Explain intermediate code generation.", 10.0));

        Exam created = examService.createExam(exam, questions, faculty);

        assertThat(created.getId()).isNotNull();
        assertThat(created.getStatus()).isEqualTo(ExamStatus.DRAFT);
        assertThat(examService.getQuestionsForExam(created.getId())).hasSize(2);
    }

    @Test
    @DisplayName("Publish exam transitions DRAFT -> PUBLISHED when questions exist")
    void testPublishExamSuccess() {
        Exam exam = new Exam("Computer Networks", "CS305", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.DRAFT);
        Exam created = examRepository.save(exam);

        questionRepository.save(new Question(created, 1, "Explain TCP 3-way handshake.", 10.0));

        Exam published = examService.publishExam(created.getId(), faculty);

        assertThat(published.getStatus()).isEqualTo(ExamStatus.PUBLISHED);
    }

    @Test
    @DisplayName("Publishing an examination with zero questions throws ValidationException")
    void testPublishExamFailsWithZeroQuestions() {
        Exam exam = new Exam("Empty Exam", "CS999", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.DRAFT);
        Exam created = examRepository.save(exam);

        assertThatThrownBy(() -> examService.publishExam(created.getId(), faculty))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("Cannot publish an examination with zero questions");
    }

    @Test
    @DisplayName("Open re-evaluation transitions PUBLISHED -> RE_EVALUATION_OPEN with valid window")
    void testOpenReevaluationFromPublished() {
        Exam exam = new Exam("Database Systems", "CS303", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.PUBLISHED);
        Exam created = examRepository.save(exam);

        LocalDateTime start = LocalDateTime.now();
        LocalDateTime end = start.plusDays(5);

        Exam openExam = examService.openReevaluation(created.getId(), start, end, faculty);

        assertThat(openExam.getStatus()).isEqualTo(ExamStatus.RE_EVALUATION_OPEN);
        assertThat(openExam.getReevaluationStart()).isEqualTo(start);
        assertThat(openExam.getReevaluationEnd()).isEqualTo(end);
    }

    @Test
    @DisplayName("Opening re-evaluation on a DRAFT exam throws InvalidStateTransitionException")
    void testOpenReevaluationFailsFromDraft() {
        Exam exam = new Exam("Draft Exam", "CS101", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.DRAFT);
        Exam created = examRepository.save(exam);

        assertThatThrownBy(() -> examService.openReevaluation(created.getId(), LocalDateTime.now(), LocalDateTime.now().plusDays(7), faculty))
                .isInstanceOf(InvalidStateTransitionException.class)
                .hasMessageContaining("Re-evaluation can only be opened for PUBLISHED examinations");
    }

    @Test
    @DisplayName("Close re-evaluation transitions RE_EVALUATION_OPEN -> RE_EVALUATION_CLOSED")
    void testCloseReevaluation() {
        Exam exam = new Exam("Algorithms", "CS202", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        Exam created = examRepository.save(exam);

        Exam closed = examService.closeReevaluation(created.getId(), faculty);

        assertThat(closed.getStatus()).isEqualTo(ExamStatus.RE_EVALUATION_CLOSED);
    }

    @Test
    @DisplayName("Invalid state transition: CLOSED cannot transition back to DRAFT")
    void testInvalidTransitionFromClosedToDraft() {
        Exam exam = new Exam("Algorithms", "CS202", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.RE_EVALUATION_CLOSED);
        Exam created = examRepository.save(exam);

        assertThatThrownBy(() -> examService.updateStatus(created.getId(), ExamStatus.DRAFT, faculty))
                .isInstanceOf(InvalidStateTransitionException.class)
                .hasMessageContaining("Invalid transition from RE_EVALUATION_CLOSED to DRAFT");
    }

    @Test
    @DisplayName("Edit examination metadata succeeds in DRAFT status")
    void testEditExamMetadataInDraft() {
        Exam exam = new Exam("Old Title", "CS100", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.DRAFT);
        Exam created = examRepository.save(exam);

        Exam updated = examService.updateExam(created.getId(), "New Verified Title", "CS100-Advanced", LocalDate.now(), LocalDate.now().plusDays(12), faculty);

        assertThat(updated.getName()).isEqualTo("New Verified Title");
        assertThat(updated.getSubject()).isEqualTo("CS100-Advanced");
    }

    @Test
    @DisplayName("Edit examination metadata fails when RE_EVALUATION_OPEN")
    void testEditExamMetadataFailsWhenReevaluationOpen() {
        Exam exam = new Exam("Live Exam", "CS100", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        Exam created = examRepository.save(exam);

        assertThatThrownBy(() -> examService.updateExam(created.getId(), "Tampered Title", "CS100", LocalDate.now(), LocalDate.now().plusDays(5), faculty))
                .isInstanceOf(InvalidStateTransitionException.class)
                .hasMessageContaining("Cannot edit examination metadata once re-evaluation has commenced");
    }

    @Test
    @DisplayName("Add question to exam in DRAFT validates positive max marks")
    void testAddQuestionToExam() {
        Exam exam = new Exam("Discrete Math", "MA201", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.DRAFT);
        Exam created = examRepository.save(exam);

        Question q = examService.addQuestionToExam(created.getId(), 1, "Prove graph Euler path theorem.", 10.0, faculty);

        assertThat(q.getId()).isNotNull();
        assertThat(q.getQuestionNumber()).isEqualTo(1);
        assertThat(q.getMaxMarks()).isEqualTo(10.0);

        assertThatThrownBy(() -> examService.addQuestionToExam(created.getId(), 2, "Invalid question", -5.0, faculty))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("Maximum marks must be strictly greater than 0");
    }

    @Test
    @DisplayName("Student cannot perform faculty/admin examination operations")
    void testUnauthorizedUserCannotModifyExam() {
        Exam exam = new Exam("Software Engineering", "CS402", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.DRAFT);
        Exam created = examRepository.save(exam);

        assertThatThrownBy(() -> examService.publishExam(created.getId(), student))
                .isInstanceOf(UnauthorizedAccessException.class)
                .hasMessageContaining("Only Faculty or Administrators can perform this examination operation");
    }
}
