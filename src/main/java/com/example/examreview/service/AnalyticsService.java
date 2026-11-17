package com.example.examreview.service;

import com.example.examreview.dto.ExamAnalyticsDto;
import com.example.examreview.dto.QuestionAnalyticsDto;
import com.example.examreview.entity.*;
import com.example.examreview.exception.ResourceNotFoundException;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.repository.*;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class AnalyticsService {

    private final ExamRepository examRepository;
    private final QuestionRepository questionRepository;
    private final RecheckRequestRepository recheckRequestRepository;
    private final StudentResultRepository studentResultRepository;
    private final UserRepository userRepository;

    public AnalyticsService(ExamRepository examRepository,
                            QuestionRepository questionRepository,
                            RecheckRequestRepository recheckRequestRepository,
                            StudentResultRepository studentResultRepository,
                            UserRepository userRepository) {
        this.examRepository = examRepository;
        this.questionRepository = questionRepository;
        this.recheckRequestRepository = recheckRequestRepository;
        this.studentResultRepository = studentResultRepository;
        this.userRepository = userRepository;
    }

    public ExamAnalyticsDto getExamAnalytics(Long examId, int threshold, User actor) {
        validateFacultyOrAdmin(actor);

        Exam exam = examRepository.findById(examId)
                .orElseThrow(() -> new ResourceNotFoundException("Examination not found with ID: " + examId));

        if (threshold < 1 || threshold > 100) {
            threshold = 30; // fallback to default
        }

        List<StudentResult> enrolledResults = studentResultRepository.findByExamId(examId);
        long cohortSize = enrolledResults.size();
        if (cohortSize == 0) {
            long totalStudents = userRepository.findByRole(Role.STUDENT).size();
            cohortSize = totalStudents > 0 ? totalStudents : 1;
        }

        List<RecheckRequest> allExamRequests = recheckRequestRepository.findByExamIdOrderByCreatedAtDesc(examId);
        long totalRequests = allExamRequests.size();
        long pendingRequests = allExamRequests.stream()
                .filter(r -> r.getStatus() == RequestStatus.SUBMITTED || r.getStatus() == RequestStatus.UNDER_REVIEW)
                .count();
        long approvedRequests = allExamRequests.stream()
                .filter(r -> r.getStatus() == RequestStatus.APPROVED)
                .count();
        long rejectedRequests = allExamRequests.stream()
                .filter(r -> r.getStatus() == RequestStatus.REJECTED)
                .count();

        // Efficient single-query aggregated counts per question
        List<Object[]> aggregatedCounts = recheckRequestRepository.countRequestsByQuestionForExam(examId);
        Map<Long, Long> countsMap = new HashMap<>();
        for (Object[] row : aggregatedCounts) {
            countsMap.put((Long) row[0], (Long) row[1]);
        }

        List<Question> questions = questionRepository.findByExamIdOrderByQuestionNumberAsc(examId);
        List<QuestionAnalyticsDto> questionStats = new ArrayList<>();

        for (Question q : questions) {
            long count = countsMap.getOrDefault(q.getId(), 0L);
            double percentage = ((double) count / cohortSize) * 100.0;
            boolean isFlagged = percentage >= threshold;
            questionStats.add(new QuestionAnalyticsDto(q, count, percentage, isFlagged));
        }

        return new ExamAnalyticsDto(
                exam,
                totalRequests,
                pendingRequests,
                approvedRequests,
                rejectedRequests,
                cohortSize,
                threshold,
                questionStats
        );
    }

    public List<QuestionAnalyticsDto> getHighDisputeQuestions(Long examId, int threshold, User actor) {
        ExamAnalyticsDto analytics = getExamAnalytics(examId, threshold, actor);
        return analytics.getQuestionStats().stream()
                .filter(QuestionAnalyticsDto::isFlagged)
                .toList();
    }

    private void validateFacultyOrAdmin(User user) {
        if (user == null || (user.getRole() != Role.FACULTY && user.getRole() != Role.ADMIN)) {
            throw new UnauthorizedAccessException("Only faculty members or administrators can access examination dispute analytics.");
        }
    }
}
