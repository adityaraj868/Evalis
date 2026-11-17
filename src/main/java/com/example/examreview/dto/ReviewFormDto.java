package com.example.examreview.dto;

import com.example.examreview.entity.ReviewDecision;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class ReviewFormDto {

    @NotNull(message = "Review decision is required.")
    private ReviewDecision decision;

    private Double revisedMarks;

    @Size(max = 2000, message = "Comments must not exceed 2000 characters.")
    private String comments;

    public ReviewFormDto() {}

    public ReviewFormDto(ReviewDecision decision, Double revisedMarks, String comments) {
        this.decision = decision;
        this.revisedMarks = revisedMarks;
        this.comments = comments;
    }

    public ReviewDecision getDecision() { return decision; }
    public void setDecision(ReviewDecision decision) { this.decision = decision; }

    public Double getRevisedMarks() { return revisedMarks; }
    public void setRevisedMarks(Double revisedMarks) { this.revisedMarks = revisedMarks; }

    public String getComments() { return comments; }
    public void setComments(String comments) { this.comments = comments; }
}
