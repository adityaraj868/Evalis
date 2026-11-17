package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
public class AuditTrailTests {

    @Autowired
    private AuditService auditService;

    @Autowired
    private AuditLogRepository auditLogRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RecheckRequestRepository recheckRequestRepository;

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private QuestionMarkRepository questionMarkRepository;

    @Autowired
    private StudentResultRepository studentResultRepository;

    @Autowired
    private QuestionRepository questionRepository;

    @Autowired
    private ExamRepository examRepository;

    private User admin;
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

        admin = userRepository.save(new User("Admin System", "admin_audit@example.com", "pass", Role.ADMIN));
        faculty = userRepository.save(new User("Faculty Evaluator", "faculty_audit@example.com", "pass", Role.FACULTY));
        student = userRepository.save(new User("Audited Student", "student_audit@example.com", "pass", Role.STUDENT));
    }

    @Test
    @DisplayName("Create structured audit log with resource type, resource ID, before/after values")
    void testCreateStructuredAuditLog() {
        AuditLog log = auditService.log(
                faculty,
                "MARKS_REVISED",
                "MARKS",
                101L,
                "4.0",
                "7.5",
                "Revised marks for question 1 from 4.0 to 7.5"
        );

        assertThat(log).isNotNull();
        assertThat(log.getId()).isNotNull();
        assertThat(log.getAction()).isEqualTo("MARKS_REVISED");
        assertThat(log.getResourceType()).isEqualTo("MARKS");
        assertThat(log.getResourceId()).isEqualTo(101L);
        assertThat(log.getPreviousValue()).isEqualTo("4.0");
        assertThat(log.getUpdatedValue()).isEqualTo("7.5");
        assertThat(log.getTimestamp()).isNotNull();
        assertThat(log.getUser().getEmail()).isEqualTo("faculty_audit@example.com");
    }

    @Test
    @DisplayName("Filter audit logs by action type")
    void testFilterAuditLogsByAction() {
        auditService.log(admin, "EXAM_CREATED", "EXAM", 1L, null, "DRAFT", "Created exam 1");
        auditService.log(faculty, "MARKS_REVISED", "MARKS", 2L, "3.0", "6.0", "Revised mark");
        auditService.log(admin, "EXAM_PUBLISHED", "EXAM", 1L, "DRAFT", "PUBLISHED", "Published exam 1");

        List<AuditLog> examCreatedLogs = auditService.filterLogs("EXAM_CREATED", null, null);
        assertThat(examCreatedLogs).hasSize(1);
        assertThat(examCreatedLogs.get(0).getAction()).isEqualTo("EXAM_CREATED");

        List<AuditLog> marksRevisedLogs = auditService.filterLogs("MARKS_REVISED", null, null);
        assertThat(marksRevisedLogs).hasSize(1);
        assertThat(marksRevisedLogs.get(0).getAction()).isEqualTo("MARKS_REVISED");
    }

    @Test
    @DisplayName("Filter audit logs by resource type")
    void testFilterAuditLogsByResourceType() {
        auditService.log(admin, "EXAM_CREATED", "EXAM", 1L, null, "DRAFT", "Created exam");
        auditService.log(student, "REQUEST_SUBMITTED", "REQUEST", 50L, null, "SUBMITTED", "Filed request");
        auditService.log(faculty, "REVIEW_COMPLETED", "REVIEW", 99L, null, "APPROVED", "Approved review");

        List<AuditLog> examLogs = auditService.filterLogs(null, "EXAM", null);
        assertThat(examLogs).hasSize(1);
        assertThat(examLogs.get(0).getResourceType()).isEqualTo("EXAM");

        List<AuditLog> requestLogs = auditService.filterLogs(null, "REQUEST", null);
        assertThat(requestLogs).hasSize(1);
        assertThat(requestLogs.get(0).getResourceType()).isEqualTo("REQUEST");
    }

    @Test
    @DisplayName("Filter audit logs by user ID")
    void testFilterAuditLogsByUser() {
        auditService.log(faculty, "MARK_RECORDED", "MARKS", 1L, null, "8.0", "Entered mark");
        auditService.log(student, "REQUEST_SUBMITTED", "REQUEST", 2L, null, "SUBMITTED", "Filed request");

        List<AuditLog> studentLogs = auditService.filterLogs(null, null, student.getId());
        assertThat(studentLogs).hasSize(1);
        assertThat(studentLogs.get(0).getUser().getId()).isEqualTo(student.getId());

        List<AuditLog> facultyLogs = auditService.filterLogs(null, null, faculty.getId());
        assertThat(facultyLogs).hasSize(1);
        assertThat(facultyLogs.get(0).getUser().getId()).isEqualTo(faculty.getId());
    }

    @Test
    @DisplayName("Audit log chronological retrieval orders latest events first")
    void testChronologicalOrdering() {
        AuditLog first = auditService.log(admin, "SYSTEM_INIT", "Initialization");
        AuditLog second = auditService.log(faculty, "EXAM_CREATED", "New exam");

        List<AuditLog> logs = auditService.getAllLogs();
        assertThat(logs).hasSize(2);
        // Latest first
        assertThat(logs.get(0).getAction()).isEqualTo("EXAM_CREATED");
        assertThat(logs.get(1).getAction()).isEqualTo("SYSTEM_INIT");
    }
}
