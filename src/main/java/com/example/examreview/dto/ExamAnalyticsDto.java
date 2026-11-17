package com.example.examreview.dto;

import com.example.examreview.entity.Exam;

import java.util.List;

public class ExamAnalyticsDto {

    private final Exam exam;
    private final long totalRequests;
    private final long pendingRequests;
    private final long approvedRequests;
    private final long rejectedRequests;
    private final long cohortSize;
    private final int threshold;
    private final List<QuestionAnalyticsDto> questionStats;

    public ExamAnalyticsDto(Exam exam,
                            long totalRequests,
                            long pendingRequests,
                            long approvedRequests,
                            long rejectedRequests,
                            long cohortSize,
                            int threshold,
                            List<QuestionAnalyticsDto> questionStats) {
        this.exam = exam;
        this.totalRequests = totalRequests;
        this.pendingRequests = pendingRequests;
        this.approvedRequests = approvedRequests;
        this.rejectedRequests = rejectedRequests;
        this.cohortSize = cohortSize;
        this.threshold = threshold;
        this.questionStats = questionStats;
    }

    public Exam getExam() { return exam; }
    public long getTotalRequests() { return totalRequests; }
    public long getPendingRequests() { return pendingRequests; }
    public long getApprovedRequests() { return approvedRequests; }
    public long getRejectedRequests() { return rejectedRequests; }
    public long getCohortSize() { return cohortSize; }
    public int getThreshold() { return threshold; }
    public List<QuestionAnalyticsDto> getQuestionStats() { return questionStats; }
}
