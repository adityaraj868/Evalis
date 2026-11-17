package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.exception.DuplicateRequestException;
import com.example.examreview.exception.InvalidStateTransitionException;
import com.example.examreview.exception.ResourceNotFoundException;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.exception.ValidationException;
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
        if (student == null || student.getRole() != Role.STUDENT) {
            throw new UnauthorizedAccessException("Only enrolled students can submit re-evaluation requests.");
        }

        if (reason == null || reason.trim().length() < 5) {
            throw new ValidationException("A clear and descriptive justification of at least 5 characters is required.");
        }

        Question question = questionRepository.findById(questionId)
                .orElseThrow(() -> new ResourceNotFoundException("Question not found with ID: " + questionId));

        Exam exam = question.getExam();
        if (!exam.getId().equals(examId)) {
            throw new ValidationException("Selected question does not belong to the specified examination.");
        }

        // Validate examination status
        if (exam.getStatus() != ExamStatus.RE_EVALUATION_OPEN) {
            throw new InvalidStateTransitionException("Re-evaluation window is not currently open for this examination. Current status: " + exam.getStatus());
        }

        // Validate time window
        LocalDateTime now = LocalDateTime.now();
        if (exam.getReevaluationStart() != null && now.isBefore(exam.getReevaluationStart())) {
            throw new InvalidStateTransitionException("Re-evaluation window has not commenced yet. Starts: " + exam.getReevaluationStart());
        }
        if (exam.getReevaluationEnd() != null && now.isAfter(exam.getReevaluationEnd())) {
            throw new InvalidStateTransitionException("Re-evaluation window has already concluded. Ended: " + exam.getReevaluationEnd());
        }

        // Student must be enrolled with results on record
        if (!studentResultRepository.existsByStudentIdAndExamId(student.getId(), examId)) {
            throw new UnauthorizedAccessException("Student has no examination result or enrollment on record for this exam.");
        }

        // Valid mark entry must exist for this question
        if (!questionMarkRepository.existsByStudentIdAndQuestionId(student.getId(), questionId)) {
            throw new ValidationException("No evaluation mark entry found for this student and question.");
        }

        // Duplicate check (Application level check)
        if (recheckRequestRepository.existsByStudentIdAndExamIdAndQuestionId(student.getId(), examId, questionId)) {
            throw new DuplicateRequestException("A re-evaluation request has already been submitted for this question.");
        }

        // Database constraint level safety (handles concurrent submissions)
        try {
            RecheckRequest request = new RecheckRequest(student, exam, question, reason.trim());
            request.setStatus(RequestStatus.SUBMITTED);
            RecheckRequest saved = recheckRequestRepository.saveAndFlush(request);

            auditService.log(student, "REQUEST_SUBMITTED",
                    String.format("Submitted re-evaluation request ID %d for Question %d in exam '%s'",
                            saved.getId(), question.getQuestionNumber(), exam.getName()));

            return saved;
        } catch (DataIntegrityViolationException ex) {
            throw new DuplicateRequestException("A re-evaluation request already exists for this question (concurrent submission conflict).");
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

    @Transactional
    public RecheckRequest markUnderReview(Long requestId, User actor) {
        RecheckRequest request = recheckRequestRepository.findById(requestId)
                .orElseThrow(() -> new ResourceNotFoundException("Request not found with ID: " + requestId));

        if (request.getStatus() == RequestStatus.SUBMITTED) {
            request.setStatus(RequestStatus.UNDER_REVIEW);
            recheckRequestRepository.save(request);
            auditService.log(actor, "REQUEST_UNDER_REVIEW",
                    String.format("Re-evaluation request ID %d is now UNDER_REVIEW by %s", requestId, actor != null ? actor.getName() : "System"));
        }
        return request;
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
