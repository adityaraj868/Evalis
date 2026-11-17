package com.example.examreview.service;

import com.example.examreview.dto.ExamAnalyticsDto;
import com.example.examreview.dto.QuestionAnalyticsDto;
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
public class QuestionAnalyticsTests {

    @Autowired
    private AnalyticsService analyticsService;

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
    private User student3;
    private Exam exam;
    private Question q1;
    private Question q2;

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

        faculty = userRepository.save(new User("Prof. Babbage", "babbage_an@example.com", "pass", Role.FACULTY));
        student1 = userRepository.save(new User("Student One", "s1_an@example.com", "pass", Role.STUDENT));
        student2 = userRepository.save(new User("Student Two", "s2_an@example.com", "pass", Role.STUDENT));
        student3 = userRepository.save(new User("Student Three", "s3_an@example.com", "pass", Role.STUDENT));

        exam = new Exam("Discrete Structures", "CS102", LocalDate.now(), LocalDate.now().plusDays(10));
        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        exam.setReevaluationStart(LocalDateTime.now().minusDays(1));
        exam.setReevaluationEnd(LocalDateTime.now().plusDays(7));
        exam = examRepository.save(exam);

        q1 = questionRepository.save(new Question(exam, 1, "Graph Isomorphism Proof.", 10.0));
        q2 = questionRepository.save(new Question(exam, 2, "Recurrence Relation Solution.", 10.0));

        // Enroll all 3 students with marks
        marksService.recordMark(student1, q1, 3.0, faculty);
        marksService.recordMark(student1, q2, 8.0, faculty);

        marksService.recordMark(student2, q1, 2.0, faculty);
        marksService.recordMark(student2, q2, 7.0, faculty);

        marksService.recordMark(student3, q1, 4.0, faculty);
        marksService.recordMark(student3, q2, 9.0, faculty);
    }

    @Test
    @DisplayName("Analytics aggregates request counts by status (total, pending, approved, rejected)")
    void testAnalyticsAggregationCorrectness() {
        // student1 requests review for Q1
        RecheckRequest r1 = recheckRequestService.submitRequest(student1, exam.getId(), q1.getId(),
                "Graph degree sequence was correctly checked.");
        // student2 requests review for Q1
        RecheckRequest r2 = recheckRequestService.submitRequest(student2, exam.getId(), q1.getId(),
                "Complement graph mapping step was valid.");

        // Faculty approves r1, r2 remains SUBMITTED (pending)
        reviewService.processReview(r1.getId(), faculty, ReviewDecision.APPROVED, "Verified complement graph.", 6.0);

        ExamAnalyticsDto analytics = analyticsService.getExamAnalytics(exam.getId(), 30, faculty);

        assertThat(analytics.getTotalRequests()).isEqualTo(2);
        assertThat(analytics.getApprovedRequests()).isEqualTo(1);
        assertThat(analytics.getPendingRequests()).isEqualTo(1);
        assertThat(analytics.getRejectedRequests()).isEqualTo(0);
        assertThat(analytics.getCohortSize()).isEqualTo(3);
    }

    @Test
    @DisplayName("High dispute question is flagged when request percentage exceeds threshold")
    void testQuestionDisputeRateAndThresholdFlagging() {
        // 2 out of 3 students dispute Q1 -> 66.7% dispute rate
        recheckRequestService.submitRequest(student1, exam.getId(), q1.getId(), "Dispute reason 1 for Q1");
        recheckRequestService.submitRequest(student2, exam.getId(), q1.getId(), "Dispute reason 2 for Q1");

        // 0 students dispute Q2 -> 0.0% dispute rate

        ExamAnalyticsDto analytics = analyticsService.getExamAnalytics(exam.getId(), 50, faculty);

        List<QuestionAnalyticsDto> stats = analytics.getQuestionStats();
        assertThat(stats).hasSize(2);

        QuestionAnalyticsDto q1Stat = stats.stream().filter(s -> s.getQuestion().getId().equals(q1.getId())).findFirst().orElseThrow();
        assertThat(q1Stat.getRequestCount()).isEqualTo(2);
        assertThat(q1Stat.getDisputePercentage()).isCloseTo(66.66, org.assertj.core.data.Offset.offset(0.1));
        assertThat(q1Stat.isFlagged()).isTrue(); // 66.7% >= 50% threshold

        QuestionAnalyticsDto q2Stat = stats.stream().filter(s -> s.getQuestion().getId().equals(q2.getId())).findFirst().orElseThrow();
        assertThat(q2Stat.getRequestCount()).isEqualTo(0);
        assertThat(q2Stat.getDisputePercentage()).isEqualTo(0.0);
        assertThat(q2Stat.isFlagged()).isFalse();
    }

    @Test
    @DisplayName("getHighDisputeQuestions filters only flagged questions")
    void testHighDisputeQuestionsFilter() {
        recheckRequestService.submitRequest(student1, exam.getId(), q1.getId(), "Dispute reason 1");
        recheckRequestService.submitRequest(student2, exam.getId(), q1.getId(), "Dispute reason 2");

        List<QuestionAnalyticsDto> highDispute = analyticsService.getHighDisputeQuestions(exam.getId(), 40, faculty);

        assertThat(highDispute).hasSize(1);
        assertThat(highDispute.get(0).getQuestion().getId()).isEqualTo(q1.getId());
    }

    @Test
    @DisplayName("Empty dataset handling: zero requests produces zero counts and percentages without error")
    void testEmptyDatasetAnalytics() {
        ExamAnalyticsDto analytics = analyticsService.getExamAnalytics(exam.getId(), 30, faculty);

        assertThat(analytics.getTotalRequests()).isEqualTo(0);
        assertThat(analytics.getPendingRequests()).isEqualTo(0);
        for (QuestionAnalyticsDto s : analytics.getQuestionStats()) {
            assertThat(s.getRequestCount()).isEqualTo(0);
            assertThat(s.getDisputePercentage()).isEqualTo(0.0);
            assertThat(s.isFlagged()).isFalse();
        }
    }

    @Test
    @DisplayName("Non-faculty user cannot access analytics")
    void testNonFacultyCannotAccessAnalytics() {
        assertThatThrownBy(() -> analyticsService.getExamAnalytics(exam.getId(), 30, student1))
                .isInstanceOf(UnauthorizedAccessException.class)
                .hasMessageContaining("Only faculty members or administrators can access examination dispute analytics");
    }
}
