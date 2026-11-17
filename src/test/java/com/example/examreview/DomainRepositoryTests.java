package com.example.examreview;

import com.example.examreview.entity.*;
import com.example.examreview.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@DataJpaTest
@ActiveProfiles("test")
class DomainRepositoryTests {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ExamRepository examRepository;

    @Autowired
    private QuestionRepository questionRepository;

    @Autowired
    private StudentResultRepository studentResultRepository;

    @Autowired
    private QuestionMarkRepository questionMarkRepository;

    @Autowired
    private RecheckRequestRepository recheckRequestRepository;

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private AuditLogRepository auditLogRepository;

    private User student;
    private User faculty;
    private Exam exam;
    private Question question1;
    private Question question2;

    @BeforeEach
    void setUp() {
        student = new User("Alice Student", "alice@example.com", "secretHash", Role.STUDENT);
        faculty = new User("Dr. Bob Faculty", "bob@example.com", "secretHash", Role.FACULTY);
        entityManager.persist(student);
        entityManager.persist(faculty);

        exam = new Exam("Midterm 2026", "Computer Science", LocalDate.now(), LocalDate.now().plusDays(7));
        exam.setStatus(ExamStatus.PUBLISHED);
        exam.setReevaluationStart(LocalDateTime.now().minusHours(1));
        exam.setReevaluationEnd(LocalDateTime.now().plusDays(3));
        entityManager.persist(exam);

        question1 = new Question(exam, 1, "What is polymorphism?", 10.0);
        question2 = new Question(exam, 2, "Explain ACID properties.", 15.0);
        entityManager.persist(question1);
        entityManager.persist(question2);

        entityManager.flush();
    }

    @Test
    @DisplayName("User repository finds by email and checks existence")
    void testUserRepository() {
        Optional<User> found = userRepository.findByEmail("alice@example.com");
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Alice Student");
        assertThat(found.get().getRole()).isEqualTo(Role.STUDENT);
        assertThat(found.get().isActive()).isTrue();
        assertThat(found.get().getCreatedAt()).isNotNull();

        assertThat(userRepository.existsByEmail("alice@example.com")).isTrue();
        assertThat(userRepository.existsByEmail("nonexistent@example.com")).isFalse();

        List<User> facultyList = userRepository.findByRole(Role.FACULTY);
        assertThat(facultyList).hasSize(1);
        assertThat(facultyList.get(0).getEmail()).isEqualTo("bob@example.com");
    }

    @Test
    @DisplayName("Exam and question relationships persist and order properly")
    void testExamAndQuestions() {
        List<Question> questions = questionRepository.findByExamIdOrderByQuestionNumberAsc(exam.getId());
        assertThat(questions).hasSize(2);
        assertThat(questions.get(0).getQuestionNumber()).isEqualTo(1);
        assertThat(questions.get(1).getQuestionNumber()).isEqualTo(2);
    }

    @Test
    @DisplayName("StudentResult saves and enforces UNIQUE(student_id, exam_id)")
    void testStudentResultUniqueConstraint() {
        StudentResult result = new StudentResult(student, exam, 22.0);
        studentResultRepository.saveAndFlush(result);

        assertThat(result.getId()).isNotNull();
        assertThat(studentResultRepository.findByStudentIdAndExamId(student.getId(), exam.getId())).isPresent();

        StudentResult duplicate = new StudentResult(student, exam, 25.0);
        assertThatThrownBy(() -> studentResultRepository.saveAndFlush(duplicate))
                .isInstanceOf(DataIntegrityViolationException.class);
    }

    @Test
    @DisplayName("QuestionMark saves and enforces UNIQUE(student_id, question_id)")
    void testQuestionMarkUniqueConstraint() {
        QuestionMark mark1 = new QuestionMark(student, question1, 8.5);
        questionMarkRepository.saveAndFlush(mark1);

        assertThat(mark1.getId()).isNotNull();
        assertThat(questionMarkRepository.findByStudentIdAndQuestionId(student.getId(), question1.getId())).isPresent();

        QuestionMark duplicateMark = new QuestionMark(student, question1, 9.0);
        assertThatThrownBy(() -> questionMarkRepository.saveAndFlush(duplicateMark))
                .isInstanceOf(DataIntegrityViolationException.class);
    }

    @Test
    @DisplayName("ADR-003: RecheckRequest enforces UNIQUE(student_id, exam_id, question_id)")
    void testRecheckRequestUniqueConstraint() {
        RecheckRequest request = new RecheckRequest(student, exam, question1, "Mark calculation seems incorrect for subpart b.");
        recheckRequestRepository.saveAndFlush(request);

        assertThat(request.getId()).isNotNull();
        assertThat(request.getStatus()).isEqualTo(RequestStatus.SUBMITTED);
        assertThat(request.getCreatedAt()).isNotNull();

        // Check exists
        boolean exists = recheckRequestRepository.existsByStudentIdAndExamIdAndQuestionId(
                student.getId(), exam.getId(), question1.getId());
        assertThat(exists).isTrue();

        // Duplicate submission must violate unique constraint at database level
        RecheckRequest duplicateRequest = new RecheckRequest(student, exam, question1, "Duplicate request for same question.");
        assertThatThrownBy(() -> recheckRequestRepository.saveAndFlush(duplicateRequest))
                .isInstanceOf(DataIntegrityViolationException.class);
    }

    @Test
    @DisplayName("RecheckRequest aggregation counts requests by question for an exam")
    void testRecheckRequestAggregation() {
        User student2 = new User("Charlie Student", "charlie@example.com", "secretHash", Role.STUDENT);
        entityManager.persist(student2);

        RecheckRequest req1 = new RecheckRequest(student, exam, question1, "Need review for Q1");
        RecheckRequest req2 = new RecheckRequest(student2, exam, question1, "Also need review for Q1");
        recheckRequestRepository.saveAndFlush(req1);
        recheckRequestRepository.saveAndFlush(req2);

        List<Object[]> counts = recheckRequestRepository.countRequestsByQuestionForExam(exam.getId());
        assertThat(counts).hasSize(1);
        Object[] row = counts.get(0);
        assertThat(row[0]).isEqualTo(question1.getId());
        assertThat((Long) row[1]).isEqualTo(2L);
    }

    @Test
    @DisplayName("Review saves with faculty decision and updates request history")
    void testReview() {
        RecheckRequest request = new RecheckRequest(student, exam, question1, "Discrepancy in Q1");
        entityManager.persist(request);
        entityManager.flush();

        Review review = new Review(request, faculty, ReviewDecision.APPROVED, "Verified solution key, student awarded 1 extra mark.", 9.5);
        reviewRepository.saveAndFlush(review);

        assertThat(review.getId()).isNotNull();
        assertThat(review.getReviewedAt()).isNotNull();

        List<Review> reviewsForRequest = reviewRepository.findByRequestIdOrderByReviewedAtDesc(request.getId());
        assertThat(reviewsForRequest).hasSize(1);
        assertThat(reviewsForRequest.get(0).getRevisedMarks()).isEqualTo(9.5);
        assertThat(reviewsForRequest.get(0).getDecision()).isEqualTo(ReviewDecision.APPROVED);
    }

    @Test
    @DisplayName("AuditLog records and retrieves chronological entries")
    void testAuditLog() {
        AuditLog log1 = new AuditLog(student, "REQUEST_SUBMITTED", "Submitted recheck request for Q1");
        AuditLog log2 = new AuditLog(faculty, "REVIEW_APPROVED", "Approved recheck request for Q1");

        auditLogRepository.save(log1);
        auditLogRepository.save(log2);
        auditLogRepository.flush();

        List<AuditLog> allLogs = auditLogRepository.findAllByOrderByTimestampDesc();
        assertThat(allLogs).hasSize(2);
        assertThat(auditLogRepository.findByUserIdOrderByTimestampDesc(student.getId())).hasSize(1);
    }
}
