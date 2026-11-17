package com.example.examreview.service;

import com.example.examreview.entity.Exam;
import com.example.examreview.entity.ExamStatus;
import com.example.examreview.entity.Question;
import com.example.examreview.entity.User;
import com.example.examreview.repository.ExamRepository;
import com.example.examreview.repository.QuestionRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class ExamService {

    private final ExamRepository examRepository;
    private final QuestionRepository questionRepository;
    private final AuditService auditService;

    public ExamService(ExamRepository examRepository,
                       QuestionRepository questionRepository,
                       AuditService auditService) {
        this.examRepository = examRepository;
        this.questionRepository = questionRepository;
        this.auditService = auditService;
    }

    public List<Exam> getAllExams() {
        return examRepository.findAllByOrderByCreatedAtDesc();
    }

    public List<Exam> getExamsByStatus(ExamStatus status) {
        return examRepository.findByStatus(status);
    }

    public Optional<Exam> getExamById(Long id) {
        return examRepository.findById(id);
    }

    @Transactional
    public Exam createExam(Exam exam, List<Question> questions, User actor) {
        Exam savedExam = examRepository.save(exam);
        if (questions != null) {
            for (Question q : questions) {
                savedExam.addQuestion(q);
            }
            savedExam = examRepository.save(savedExam);
        }
        auditService.log(actor, "EXAM_CREATED", "Created exam: " + savedExam.getName() + " (ID: " + savedExam.getId() + ")");
        return savedExam;
    }

    @Transactional
    public Exam updateStatus(Long examId, ExamStatus newStatus, User actor) {
        Exam exam = examRepository.findById(examId)
                .orElseThrow(() -> new IllegalArgumentException("Exam not found: " + examId));

        ExamStatus oldStatus = exam.getStatus();
        exam.setStatus(newStatus);
        examRepository.save(exam);

        auditService.log(actor, "EXAM_STATUS_UPDATED",
                String.format("Updated exam ID %d status from %s to %s", examId, oldStatus, newStatus));
        return exam;
    }

    @Transactional
    public Exam openReevaluation(Long examId, LocalDateTime start, LocalDateTime end, User actor) {
        Exam exam = examRepository.findById(examId)
                .orElseThrow(() -> new IllegalArgumentException("Exam not found: " + examId));

        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        exam.setReevaluationStart(start != null ? start : LocalDateTime.now());
        exam.setReevaluationEnd(end != null ? end : LocalDateTime.now().plusDays(7));
        examRepository.save(exam);

        auditService.log(actor, "REEVALUATION_OPENED",
                "Opened re-evaluation for exam: " + exam.getName() + " until " + exam.getReevaluationEnd());
        return exam;
    }

    @Transactional
    public Exam closeReevaluation(Long examId, User actor) {
        Exam exam = examRepository.findById(examId)
                .orElseThrow(() -> new IllegalArgumentException("Exam not found: " + examId));

        exam.setStatus(ExamStatus.RE_EVALUATION_CLOSED);
        examRepository.save(exam);

        auditService.log(actor, "REEVALUATION_CLOSED",
                "Closed re-evaluation for exam: " + exam.getName());
        return exam;
    }

    public List<Question> getQuestionsForExam(Long examId) {
        return questionRepository.findByExamIdOrderByQuestionNumberAsc(examId);
    }

    public Optional<Question> getQuestionById(Long questionId) {
        return questionRepository.findById(questionId);
    }
}
