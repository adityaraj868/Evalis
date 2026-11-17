package com.example.examreview.service;

import com.example.examreview.entity.*;
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
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
@ActiveProfiles("test")
public class MarksManagementTests {

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
    private Question q2;
    private Question q3;

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

        faculty = userRepository.save(new User("Prof. Knuth", "knuth_marks@example.com", "pass", Role.FACULTY));
        student = userRepository.save(new User("Grace Student", "grace_marks@example.com", "pass", Role.STUDENT));

        exam = examRepository.save(new Exam("Automata Theory", "CS304", LocalDate.now(), LocalDate.now().plusDays(10)));
        q1 = questionRepository.save(new Question(exam, 1, "Design DFA for binary strings divisible by 3.", 10.0));
        q2 = questionRepository.save(new Question(exam, 2, "Convert NFA to DFA with epsilon transitions.", 15.0));
        q3 = questionRepository.save(new Question(exam, 3, "Pumping Lemma proof for non-regular language.", 15.0));
    }

    @Test
    @DisplayName("Record mark for a single question updates question mark and calculates total marks")
    void testRecordMarkSuccess() {
        marksService.recordMark(student, q1, 8.5, faculty);

        Optional<QuestionMark> qmOpt = marksService.getQuestionMark(student.getId(), q1.getId());
        assertThat(qmOpt).isPresent();
        assertThat(qmOpt.get().getMarksObtained()).isEqualTo(8.5);

        Optional<StudentResult> srOpt = marksService.getStudentResult(student.getId(), exam.getId());
        assertThat(srOpt).isPresent();
        assertThat(srOpt.get().getTotalMarks()).isEqualTo(8.5);
    }

    @Test
    @DisplayName("Negative marks obtained throws ValidationException")
    void testRecordMarkNegativeThrowsValidationException() {
        assertThatThrownBy(() -> marksService.recordMark(student, q1, -2.0, faculty))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("Marks obtained cannot be negative");
    }

    @Test
    @DisplayName("Marks obtained exceeding question max marks throws ValidationException")
    void testRecordMarkExceedingMaxMarksThrowsValidationException() {
        // q1 max marks is 10.0
        assertThatThrownBy(() -> marksService.recordMark(student, q1, 12.5, faculty))
                .isInstanceOf(ValidationException.class)
                .hasMessageContaining("cannot exceed maximum question marks");
    }

    @Test
    @DisplayName("Batch record marks across multiple questions calculates accurate total in single transaction")
    void testRecordExamMarksForStudentBatch() {
        Map<Long, Double> questionMarks = new HashMap<>();
        questionMarks.put(q1.getId(), 9.0);
        questionMarks.put(q2.getId(), 14.0);
        questionMarks.put(q3.getId(), 12.5);

        StudentResult result = marksService.recordExamMarksForStudent(exam.getId(), student.getId(), questionMarks, faculty);

        assertThat(result).isNotNull();
        assertThat(result.getTotalMarks()).isEqualTo(35.5);

        List<QuestionMark> marksList = marksService.getQuestionMarksForExam(student.getId(), exam.getId());
        assertThat(marksList).hasSize(3);
    }

    @Test
    @DisplayName("Update marks after review revision recalculates total student result atomically")
    void testUpdateMarksAfterReviewRecalculatesTotal() {
        Map<Long, Double> initialMarks = new HashMap<>();
        initialMarks.put(q1.getId(), 6.0);
        initialMarks.put(q2.getId(), 10.0);
        marksService.recordExamMarksForStudent(exam.getId(), student.getId(), initialMarks, faculty);

        StudentResult beforeReview = marksService.getStudentResult(student.getId(), exam.getId()).orElseThrow();
        assertThat(beforeReview.getTotalMarks()).isEqualTo(16.0);

        // Faculty awards 9.0 on q1 instead of 6.0
        marksService.updateMarksAfterReview(student.getId(), q1.getId(), 9.0, faculty);

        StudentResult afterReview = marksService.getStudentResult(student.getId(), exam.getId()).orElseThrow();
        assertThat(afterReview.getTotalMarks()).isEqualTo(19.0);

        QuestionMark updatedQm = marksService.getQuestionMark(student.getId(), q1.getId()).orElseThrow();
        assertThat(updatedQm.getMarksObtained()).isEqualTo(9.0);
    }

    @Test
    @DisplayName("Student cannot record or modify marks")
    void testNonFacultyCannotRecordMarks() {
        assertThatThrownBy(() -> marksService.recordMark(student, q1, 8.0, student))
                .isInstanceOf(UnauthorizedAccessException.class)
                .hasMessageContaining("Only Faculty or Administrators can record or modify examination marks");
    }
}
