package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.exception.ResourceNotFoundException;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.exception.ValidationException;
import com.example.examreview.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
public class MarksService {

    private final StudentResultRepository studentResultRepository;
    private final QuestionMarkRepository questionMarkRepository;
    private final QuestionRepository questionRepository;
    private final ExamRepository examRepository;
    private final UserRepository userRepository;
    private final AuditService auditService;

    public MarksService(StudentResultRepository studentResultRepository,
                        QuestionMarkRepository questionMarkRepository,
                        QuestionRepository questionRepository,
                        ExamRepository examRepository,
                        UserRepository userRepository,
                        AuditService auditService) {
        this.studentResultRepository = studentResultRepository;
        this.questionMarkRepository = questionMarkRepository;
        this.questionRepository = questionRepository;
        this.examRepository = examRepository;
        this.userRepository = userRepository;
        this.auditService = auditService;
    }

    public Optional<StudentResult> getStudentResult(Long studentId, Long examId) {
        return studentResultRepository.findByStudentIdAndExamId(studentId, examId);
    }

    public List<StudentResult> getStudentResults(Long studentId) {
        return studentResultRepository.findByStudentId(studentId);
    }

    public List<StudentResult> getExamResults(Long examId) {
        return studentResultRepository.findByExamId(examId);
    }

    public List<QuestionMark> getQuestionMarksForExam(Long studentId, Long examId) {
        return questionMarkRepository.findByQuestionExamIdAndStudentId(examId, studentId);
    }

    public Optional<QuestionMark> getQuestionMark(Long studentId, Long questionId) {
        return questionMarkRepository.findByStudentIdAndQuestionId(studentId, questionId);
    }

    @Transactional
    public void recordMark(User student, Question question, Double marksObtained) {
        // Backwards-compatible overload used by DataInitializer
        validateMarkBounds(question, marksObtained);

        Optional<QuestionMark> existing = questionMarkRepository.findByStudentIdAndQuestionId(student.getId(), question.getId());
        QuestionMark mark;
        if (existing.isPresent()) {
            mark = existing.get();
            mark.setMarksObtained(marksObtained);
        } else {
            mark = new QuestionMark(student, question, marksObtained);
        }
        questionMarkRepository.save(mark);

        Exam exam = question.getExam();
        recalculateStudentResult(student, exam);
    }

    @Transactional
    public void recordMark(User student, Question question, Double marksObtained, User actor) {
        validateFacultyOrAdmin(actor);
        validateMarkBounds(question, marksObtained);

        Optional<QuestionMark> existing = questionMarkRepository.findByStudentIdAndQuestionId(student.getId(), question.getId());
        QuestionMark mark;
        Double oldMarks = null;
        if (existing.isPresent()) {
            mark = existing.get();
            oldMarks = mark.getMarksObtained();
            mark.setMarksObtained(marksObtained);
        } else {
            mark = new QuestionMark(student, question, marksObtained);
        }
        questionMarkRepository.save(mark);

        Exam exam = question.getExam();
        recalculateStudentResult(student, exam);

        auditService.log(actor, "MARK_RECORDED",
                String.format("Recorded mark for Student ID %d on Q%d (Exam: %s): %.1f (Previous: %s)",
                        student.getId(), question.getQuestionNumber(), exam.getName(), marksObtained,
                        oldMarks != null ? String.valueOf(oldMarks) : "None"));
    }

    @Transactional
    public StudentResult recordExamMarksForStudent(Long examId, Long studentId, Map<Long, Double> questionMarks, User actor) {
        validateFacultyOrAdmin(actor);

        Exam exam = examRepository.findById(examId)
                .orElseThrow(() -> new ResourceNotFoundException("Examination not found with ID: " + examId));
        User student = userRepository.findById(studentId)
                .orElseThrow(() -> new ResourceNotFoundException("Student not found with ID: " + studentId));

        if (student.getRole() != Role.STUDENT) {
            throw new ValidationException("Marks can only be recorded for users with role STUDENT.");
        }

        List<Question> questions = questionRepository.findByExamIdOrderByQuestionNumberAsc(examId);
        Map<Long, Question> questionMap = new HashMap<>();
        for (Question q : questions) {
            questionMap.put(q.getId(), q);
        }

        double totalMarks = 0.0;
        for (Map.Entry<Long, Double> entry : questionMarks.entrySet()) {
            Long qId = entry.getKey();
            Double marks = entry.getValue();

            Question question = questionMap.get(qId);
            if (question == null) {
                throw new ValidationException("Question ID " + qId + " does not belong to examination: " + exam.getName());
            }

            validateMarkBounds(question, marks);

            Optional<QuestionMark> existingMark = questionMarkRepository.findByStudentIdAndQuestionId(studentId, qId);
            QuestionMark mark = existingMark.orElseGet(() -> new QuestionMark(student, question, marks));
            mark.setMarksObtained(marks);
            questionMarkRepository.save(mark);

            totalMarks += marks;
        }

        StudentResult result = studentResultRepository.findByStudentIdAndExamId(studentId, examId)
                .orElseGet(() -> new StudentResult(student, exam, 0.0));
        result.setTotalMarks(totalMarks);
        StudentResult savedResult = studentResultRepository.save(result);

        auditService.log(actor, "STUDENT_MARKS_RECORDED",
                String.format("Recorded total marks (%.1f) across %d questions for Student %s in exam '%s'",
                        totalMarks, questionMarks.size(), student.getName(), exam.getName()));

        return savedResult;
    }

    @Transactional
    public void updateMarksAfterReview(Long studentId, Long questionId, Double revisedMarks, User faculty) {
        validateFacultyOrAdmin(faculty);

        QuestionMark mark = questionMarkRepository.findByStudentIdAndQuestionId(studentId, questionId)
                .orElseThrow(() -> new ResourceNotFoundException("Question mark not found for student " + studentId + " and question " + questionId));

        Question question = mark.getQuestion();
        validateMarkBounds(question, revisedMarks);

        Double oldMarks = mark.getMarksObtained();
        mark.setMarksObtained(revisedMarks);
        questionMarkRepository.save(mark);

        Exam exam = question.getExam();
        User student = mark.getStudent();
        recalculateStudentResult(student, exam);

        auditService.log(faculty, "MARKS_REVISED",
                String.format("Revised marks for student ID %d, question ID %d (Exam: %s) from %.1f to %.1f",
                        studentId, questionId, exam.getName(), oldMarks, revisedMarks));
    }

    public void recalculateStudentResult(User student, Exam exam) {
        List<QuestionMark> allMarks = questionMarkRepository.findByQuestionExamIdAndStudentId(exam.getId(), student.getId());
        double total = allMarks.stream().mapToDouble(QuestionMark::getMarksObtained).sum();

        StudentResult result = studentResultRepository.findByStudentIdAndExamId(student.getId(), exam.getId())
                .orElse(new StudentResult(student, exam, total));

        result.setTotalMarks(total);
        studentResultRepository.save(result);
    }

    private void validateMarkBounds(Question question, Double marksObtained) {
        if (marksObtained == null) {
            throw new ValidationException("Marks obtained cannot be null.");
        }
        if (marksObtained < 0.0) {
            throw new ValidationException("Marks obtained cannot be negative: " + marksObtained);
        }
        Double maxMarks = question.getMaxMarks();
        if (maxMarks != null && marksObtained > maxMarks) {
            throw new ValidationException(String.format("Marks obtained (%.1f) cannot exceed maximum question marks (%.1f).",
                    marksObtained, maxMarks));
        }
    }

    private void validateFacultyOrAdmin(User user) {
        if (user == null || (user.getRole() != Role.FACULTY && user.getRole() != Role.ADMIN)) {
            throw new UnauthorizedAccessException("Only Faculty or Administrators can record or modify examination marks.");
        }
    }
}
