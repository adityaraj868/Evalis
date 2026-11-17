package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.repository.QuestionMarkRepository;
import com.example.examreview.repository.QuestionRepository;
import com.example.examreview.repository.StudentResultRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class MarksService {

    private final StudentResultRepository studentResultRepository;
    private final QuestionMarkRepository questionMarkRepository;
    private final QuestionRepository questionRepository;
    private final AuditService auditService;

    public MarksService(StudentResultRepository studentResultRepository,
                        QuestionMarkRepository questionMarkRepository,
                        QuestionRepository questionRepository,
                        AuditService auditService) {
        this.studentResultRepository = studentResultRepository;
        this.questionMarkRepository = questionMarkRepository;
        this.questionRepository = questionRepository;
        this.auditService = auditService;
    }

    public Optional<StudentResult> getStudentResult(Long studentId, Long examId) {
        return studentResultRepository.findByStudentIdAndExamId(studentId, examId);
    }

    public List<StudentResult> getStudentResults(Long studentId) {
        return studentResultRepository.findByStudentId(studentId);
    }

    public List<QuestionMark> getQuestionMarksForExam(Long studentId, Long examId) {
        return questionMarkRepository.findByQuestionExamIdAndStudentId(examId, studentId);
    }

    public Optional<QuestionMark> getQuestionMark(Long studentId, Long questionId) {
        return questionMarkRepository.findByStudentIdAndQuestionId(studentId, questionId);
    }

    @Transactional
    public void recordMark(User student, Question question, Double marksObtained) {
        Optional<QuestionMark> existing = questionMarkRepository.findByStudentIdAndQuestionId(student.getId(), question.getId());
        QuestionMark mark;
        if (existing.isPresent()) {
            mark = existing.get();
            mark.setMarksObtained(marksObtained);
        } else {
            mark = new QuestionMark(student, question, marksObtained);
        }
        questionMarkRepository.save(mark);

        // Update total marks in StudentResult
        Exam exam = question.getExam();
        recalculateStudentResult(student, exam);
    }

    @Transactional
    public void updateMarksAfterReview(Long studentId, Long questionId, Double revisedMarks, User faculty) {
        QuestionMark mark = questionMarkRepository.findByStudentIdAndQuestionId(studentId, questionId)
                .orElseThrow(() -> new IllegalArgumentException("Question mark not found for student " + studentId + " and question " + questionId));

        Double oldMarks = mark.getMarksObtained();
        mark.setMarksObtained(revisedMarks);
        questionMarkRepository.save(mark);

        Exam exam = mark.getQuestion().getExam();
        User student = mark.getStudent();
        recalculateStudentResult(student, exam);

        auditService.log(faculty, "MARKS_REVISED",
                String.format("Revised marks for student ID %d, question ID %d (Exam: %s) from %.1f to %.1f",
                        studentId, questionId, exam.getName(), oldMarks, revisedMarks));
    }

    private void recalculateStudentResult(User student, Exam exam) {
        List<QuestionMark> allMarks = questionMarkRepository.findByQuestionExamIdAndStudentId(exam.getId(), student.getId());
        double total = allMarks.stream().mapToDouble(QuestionMark::getMarksObtained).sum();

        StudentResult result = studentResultRepository.findByStudentIdAndExamId(student.getId(), exam.getId())
                .orElse(new StudentResult(student, exam, total));

        result.setTotalMarks(total);
        studentResultRepository.save(result);
    }
}
