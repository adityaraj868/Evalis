package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.exception.InvalidStateTransitionException;
import com.example.examreview.exception.ResourceNotFoundException;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.exception.ValidationException;
import com.example.examreview.repository.ExamRepository;
import com.example.examreview.repository.QuestionMarkRepository;
import com.example.examreview.repository.QuestionRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class ExamService {

    private final ExamRepository examRepository;
    private final QuestionRepository questionRepository;
    private final QuestionMarkRepository questionMarkRepository;
    private final AuditService auditService;

    public ExamService(ExamRepository examRepository,
                       QuestionRepository questionRepository,
                       QuestionMarkRepository questionMarkRepository,
                       AuditService auditService) {
        this.examRepository = examRepository;
        this.questionRepository = questionRepository;
        this.questionMarkRepository = questionMarkRepository;
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

    public Exam getRequiredExamById(Long id) {
        return examRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Examination not found with ID: " + id));
    }

    @Transactional
    public Exam createExam(Exam exam, List<Question> questions, User actor) {
        validateFacultyOrAdmin(actor);
        if (exam.getName() == null || exam.getName().trim().isEmpty()) {
            throw new ValidationException("Examination name cannot be blank.");
        }
        if (exam.getSubject() == null || exam.getSubject().trim().isEmpty()) {
            throw new ValidationException("Examination subject cannot be blank.");
        }

        if (exam.getStatus() == null) {
            exam.setStatus(ExamStatus.DRAFT);
        }

        Exam savedExam = examRepository.save(exam);
        if (questions != null) {
            int seq = 1;
            for (Question q : questions) {
                if (q.getMaxMarks() == null || q.getMaxMarks() <= 0) {
                    throw new ValidationException("Question max marks must be strictly greater than 0.");
                }
                if (q.getQuestionNumber() == null) {
                    q.setQuestionNumber(seq);
                }
                savedExam.addQuestion(q);
                seq++;
            }
            savedExam = examRepository.save(savedExam);
        }
        auditService.log(actor, "EXAM_CREATED", "Created exam: " + savedExam.getName() + " (ID: " + savedExam.getId() + ")");
        return savedExam;
    }

    @Transactional
    public Exam updateExam(Long examId, String name, String subject, LocalDate startDate, LocalDate endDate, User actor) {
        validateFacultyOrAdmin(actor);
        Exam exam = getRequiredExamById(examId);

        if (exam.getStatus() == ExamStatus.RE_EVALUATION_OPEN || exam.getStatus() == ExamStatus.RE_EVALUATION_CLOSED || exam.getStatus() == ExamStatus.ARCHIVED) {
            throw new InvalidStateTransitionException("Cannot edit examination metadata once re-evaluation has commenced or concluded.");
        }

        if (name == null || name.trim().isEmpty()) {
            throw new ValidationException("Examination name cannot be blank.");
        }
        if (subject == null || subject.trim().isEmpty()) {
            throw new ValidationException("Subject cannot be blank.");
        }

        exam.setName(name.trim());
        exam.setSubject(subject.trim());
        exam.setStartDate(startDate);
        exam.setEndDate(endDate);
        Exam updated = examRepository.save(exam);

        auditService.log(actor, "EXAM_UPDATED", "Updated exam ID: " + examId + " (" + updated.getName() + ")");
        return updated;
    }

    @Transactional
    public Exam publishExam(Long examId, User actor) {
        validateFacultyOrAdmin(actor);
        Exam exam = getRequiredExamById(examId);

        if (exam.getStatus() != ExamStatus.DRAFT) {
            throw new InvalidStateTransitionException("Only DRAFT examinations can be published. Current status: " + exam.getStatus());
        }

        List<Question> questions = questionRepository.findByExamIdOrderByQuestionNumberAsc(examId);
        if (questions.isEmpty()) {
            throw new ValidationException("Cannot publish an examination with zero questions.");
        }

        for (Question q : questions) {
            if (q.getMaxMarks() == null || q.getMaxMarks() <= 0) {
                throw new ValidationException("Question " + q.getQuestionNumber() + " has invalid max marks: " + q.getMaxMarks());
            }
        }

        exam.setStatus(ExamStatus.PUBLISHED);
        examRepository.save(exam);
        auditService.log(actor, "EXAM_PUBLISHED", "Published exam ID " + examId + " (" + exam.getName() + ") with " + questions.size() + " questions.");
        return exam;
    }

    @Transactional
    public Exam openReevaluation(Long examId, LocalDateTime start, LocalDateTime end, User actor) {
        validateFacultyOrAdmin(actor);
        Exam exam = getRequiredExamById(examId);

        if (exam.getStatus() != ExamStatus.PUBLISHED) {
            throw new InvalidStateTransitionException("Re-evaluation can only be opened for PUBLISHED examinations. Current status: " + exam.getStatus());
        }

        LocalDateTime startTime = (start != null) ? start : LocalDateTime.now();
        LocalDateTime endTime = (end != null) ? end : startTime.plusDays(7);

        if (endTime.isBefore(startTime)) {
            throw new ValidationException("Re-evaluation end date cannot be earlier than start date.");
        }

        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        exam.setReevaluationStart(startTime);
        exam.setReevaluationEnd(endTime);
        examRepository.save(exam);

        auditService.log(actor, "REEVALUATION_OPENED",
                "Opened re-evaluation for exam ID " + examId + " (" + exam.getName() + ") from " + startTime + " to " + endTime);
        return exam;
    }

    @Transactional
    public Exam closeReevaluation(Long examId, User actor) {
        validateFacultyOrAdmin(actor);
        Exam exam = getRequiredExamById(examId);

        if (exam.getStatus() != ExamStatus.RE_EVALUATION_OPEN) {
            throw new InvalidStateTransitionException("Re-evaluation can only be closed if currently OPEN. Current status: " + exam.getStatus());
        }

        exam.setStatus(ExamStatus.RE_EVALUATION_CLOSED);
        examRepository.save(exam);

        auditService.log(actor, "REEVALUATION_CLOSED",
                "Closed re-evaluation for exam ID " + examId + " (" + exam.getName() + ")");
        return exam;
    }

    @Transactional
    public Exam archiveExam(Long examId, User actor) {
        validateFacultyOrAdmin(actor);
        Exam exam = getRequiredExamById(examId);

        if (exam.getStatus() != ExamStatus.RE_EVALUATION_CLOSED) {
            throw new InvalidStateTransitionException("Only CLOSED examinations can be archived. Current status: " + exam.getStatus());
        }

        exam.setStatus(ExamStatus.ARCHIVED);
        examRepository.save(exam);

        auditService.log(actor, "EXAM_ARCHIVED", "Archived exam ID " + examId + " (" + exam.getName() + ")");
        return exam;
    }

    @Transactional
    public Exam updateStatus(Long examId, ExamStatus newStatus, User actor) {
        validateFacultyOrAdmin(actor);
        Exam exam = getRequiredExamById(examId);
        ExamStatus current = exam.getStatus();

        if (current == newStatus) {
            return exam;
        }

        // Validate state machine transitions
        switch (current) {
            case DRAFT -> {
                if (newStatus == ExamStatus.PUBLISHED) {
                    return publishExam(examId, actor);
                }
                throw new InvalidStateTransitionException("Invalid transition from DRAFT to " + newStatus);
            }
            case PUBLISHED -> {
                if (newStatus == ExamStatus.RE_EVALUATION_OPEN) {
                    return openReevaluation(examId, LocalDateTime.now(), LocalDateTime.now().plusDays(7), actor);
                }
                if (newStatus == ExamStatus.DRAFT) {
                    exam.setStatus(ExamStatus.DRAFT);
                    examRepository.save(exam);
                    auditService.log(actor, "EXAM_REVERTED_DRAFT", "Reverted exam ID " + examId + " to DRAFT");
                    return exam;
                }
                throw new InvalidStateTransitionException("Invalid transition from PUBLISHED to " + newStatus);
            }
            case RE_EVALUATION_OPEN -> {
                if (newStatus == ExamStatus.RE_EVALUATION_CLOSED) {
                    return closeReevaluation(examId, actor);
                }
                throw new InvalidStateTransitionException("Invalid transition from RE_EVALUATION_OPEN to " + newStatus);
            }
            case RE_EVALUATION_CLOSED -> {
                if (newStatus == ExamStatus.ARCHIVED) {
                    return archiveExam(examId, actor);
                }
                throw new InvalidStateTransitionException("Invalid transition from RE_EVALUATION_CLOSED to " + newStatus);
            }
            case ARCHIVED -> throw new InvalidStateTransitionException("Archived examinations cannot transition to another state.");
            default -> throw new InvalidStateTransitionException("Unknown examination status transition.");
        }
    }

    @Transactional
    public Question addQuestionToExam(Long examId, Integer questionNumber, String questionText, Double maxMarks, User actor) {
        validateFacultyOrAdmin(actor);
        Exam exam = getRequiredExamById(examId);

        if (exam.getStatus() == ExamStatus.RE_EVALUATION_OPEN || exam.getStatus() == ExamStatus.RE_EVALUATION_CLOSED || exam.getStatus() == ExamStatus.ARCHIVED) {
            throw new InvalidStateTransitionException("Cannot add questions to an examination during or after re-evaluation.");
        }

        if (questionText == null || questionText.trim().isEmpty()) {
            throw new ValidationException("Question text cannot be blank.");
        }
        if (maxMarks == null || maxMarks <= 0) {
            throw new ValidationException("Maximum marks must be strictly greater than 0.");
        }

        if (questionNumber == null || questionNumber <= 0) {
            List<Question> existing = questionRepository.findByExamIdOrderByQuestionNumberAsc(examId);
            questionNumber = existing.size() + 1;
        }

        Question question = new Question(exam, questionNumber, questionText.trim(), maxMarks);
        exam.addQuestion(question);
        Question savedQuestion = questionRepository.save(question);

        auditService.log(actor, "QUESTION_ADDED",
                "Added Question " + questionNumber + " (Max: " + maxMarks + ") to exam: " + exam.getName());
        return savedQuestion;
    }

    @Transactional
    public Question updateQuestion(Long questionId, String questionText, Double maxMarks, User actor) {
        validateFacultyOrAdmin(actor);
        Question question = questionRepository.findById(questionId)
                .orElseThrow(() -> new ResourceNotFoundException("Question not found with ID: " + questionId));

        Exam exam = question.getExam();
        if (exam.getStatus() == ExamStatus.RE_EVALUATION_OPEN || exam.getStatus() == ExamStatus.RE_EVALUATION_CLOSED || exam.getStatus() == ExamStatus.ARCHIVED) {
            throw new InvalidStateTransitionException("Cannot edit questions once re-evaluation has opened.");
        }

        if (questionText != null && !questionText.trim().isEmpty()) {
            question.setQuestionText(questionText.trim());
        }
        if (maxMarks != null) {
            if (maxMarks <= 0) {
                throw new ValidationException("Maximum marks must be strictly greater than 0.");
            }
            question.setMaxMarks(maxMarks);
        }

        Question updated = questionRepository.save(question);
        auditService.log(actor, "QUESTION_UPDATED",
                "Updated Question ID " + questionId + " in exam: " + exam.getName());
        return updated;
    }

    public List<Question> getQuestionsForExam(Long examId) {
        return questionRepository.findByExamIdOrderByQuestionNumberAsc(examId);
    }

    public Optional<Question> getQuestionById(Long questionId) {
        return questionRepository.findById(questionId);
    }

    private void validateFacultyOrAdmin(User user) {
        if (user == null || (user.getRole() != Role.FACULTY && user.getRole() != Role.ADMIN)) {
            throw new UnauthorizedAccessException("Only Faculty or Administrators can perform this examination operation.");
        }
    }
}
