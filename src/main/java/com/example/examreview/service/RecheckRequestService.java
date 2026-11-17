package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.repository.QuestionMarkRepository;
import com.example.examreview.repository.QuestionRepository;
import com.example.examreview.repository.RecheckRequestRepository;
import com.example.examreview.repository.StudentResultRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class RecheckRequestService {

    private final RecheckRequestRepository recheckRequestRepository;
    private final StudentResultRepository studentResultRepository;
    private final QuestionRepository questionRepository;
    private final QuestionMarkRepository questionMarkRepository;
    private final AuditService auditService;

    public RecheckRequestService(RecheckRequestRepository recheckRequestRepository,
                                 StudentResultRepository studentResultRepository,
                                 QuestionRepository questionRepository,
                                 QuestionMarkRepository questionMarkRepository,
                                 AuditService auditService) {
        this.recheckRequestRepository = recheckRequestRepository;
        this.studentResultRepository = studentResultRepository;
        this.questionRepository = questionRepository;
        this.questionMarkRepository = questionMarkRepository;
        this.auditService = auditService;
    }

    @Transactional
    public RecheckRequest submitRequest(User student, Long examId, Long questionId, String reason) {
        if (reason == null || reason.trim().length() < 5) {
            throw new IllegalArgumentException("A valid reason of at least 5 characters is required.");
        }

        Question question = questionRepository.findById(questionId)
                .orElseThrow(() -> new IllegalArgumentException("Question not found: " + questionId));

        Exam exam = question.getExam();
        if (!exam.getId().equals(examId)) {
            throw new IllegalArgumentException("Question does not belong to the specified examination.");
        }

        // FR-09 (3): Verify exam re-evaluation window
        if (exam.getStatus() != ExamStatus.RE_EVALUATION_OPEN) {
            throw new IllegalStateException("Re-evaluation is not currently open for this examination.");
        }
        LocalDateTime now = LocalDateTime.now();
        if (exam.getReevaluationStart() != null && now.isBefore(exam.getReevaluationStart())) {
            throw new IllegalStateException("Re-evaluation period has not started yet.");
        }
        if (exam.getReevaluationEnd() != null && now.isAfter(exam.getReevaluationEnd())) {
            throw new IllegalStateException("Re-evaluation period has already ended.");
        }

        // FR-09 (2): Student associated with examination
        if (!studentResultRepository.existsByStudentIdAndExamId(student.getId(), examId)) {
            throw new IllegalStateException("Student has no examination result on record for this exam.");
        }

        // FR-09 (5): Valid mark exists for this question
        if (!questionMarkRepository.existsByStudentIdAndQuestionId(student.getId(), questionId)) {
            throw new IllegalStateException("No mark entry found for this student and question.");
        }

        // FR-10 & ADR-003: Duplicate check (Application level)
        if (recheckRequestRepository.existsByStudentIdAndExamIdAndQuestionId(student.getId(), examId, questionId)) {
            throw new IllegalStateException("A re-evaluation request already exists for this question.");
        }

        // Persist with DB constraint safety
        try {
            RecheckRequest request = new RecheckRequest(student, exam, question, reason.trim());
            request.setStatus(RequestStatus.SUBMITTED);
            RecheckRequest saved = recheckRequestRepository.saveAndFlush(request);

            auditService.log(student, "REQUEST_SUBMITTED",
                    String.format("Submitted re-evaluation request for Question %d in exam '%s'",
                            question.getQuestionNumber(), exam.getName()));

            return saved;
        } catch (DataIntegrityViolationException ex) {
            throw new IllegalStateException("A re-evaluation request already exists for this question.", ex);
        }
    }

    public List<RecheckRequest> getStudentRequests(Long studentId) {
        return recheckRequestRepository.findByStudentIdOrderByCreatedAtDesc(studentId);
    }

    public List<RecheckRequest> getExamRequests(Long examId) {
        return recheckRequestRepository.findByExamIdOrderByCreatedAtDesc(examId);
    }

    public List<RecheckRequest> getAllRequests() {
        return recheckRequestRepository.findAll();
    }

    public Optional<RecheckRequest> getRequestById(Long id) {
        return recheckRequestRepository.findById(id);
    }

    public boolean hasExistingRequest(Long studentId, Long examId, Long questionId) {
        return recheckRequestRepository.existsByStudentIdAndExamIdAndQuestionId(studentId, examId, questionId);
    }

    public Map<Long, Long> getQuestionRequestCounts(Long examId) {
        List<Object[]> rows = recheckRequestRepository.countRequestsByQuestionForExam(examId);
        Map<Long, Long> counts = new HashMap<>();
        for (Object[] row : rows) {
            counts.put((Long) row[0], (Long) row[1]);
        }
        return counts;
    }
}
