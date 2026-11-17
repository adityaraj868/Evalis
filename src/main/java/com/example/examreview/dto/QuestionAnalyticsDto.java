package com.example.examreview.dto;

import com.example.examreview.entity.Question;

public class QuestionAnalyticsDto {

    private final Question question;
    private final long requestCount;
    private final double disputePercentage;
    private final boolean flagged;

    public QuestionAnalyticsDto(Question question, long requestCount, double disputePercentage, boolean flagged) {
        this.question = question;
        this.requestCount = requestCount;
        this.disputePercentage = disputePercentage;
        this.flagged = flagged;
    }

    public Question getQuestion() { return question; }
    public long getRequestCount() { return requestCount; }
    public double getDisputePercentage() { return disputePercentage; }
    public double getPercentage() { return disputePercentage; } // View compatibility
    public boolean isFlagged() { return flagged; }
}
