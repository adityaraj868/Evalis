package com.example.examreview.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class RecheckRequestFormDto {

    @NotNull(message = "Examination ID is required.")
    private Long examId;

    @NotNull(message = "Question ID is required.")
    private Long questionId;

    @NotBlank(message = "Reason is required.")
    @Size(min = 5, max = 2000, message = "Reason must be between 5 and 2000 characters.")
    private String reason;

    public RecheckRequestFormDto() {}

    public RecheckRequestFormDto(Long examId, Long questionId, String reason) {
        this.examId = examId;
        this.questionId = questionId;
        this.reason = reason;
    }

    public Long getExamId() { return examId; }
    public void setExamId(Long examId) { this.examId = examId; }

    public Long getQuestionId() { return questionId; }
    public void setQuestionId(Long questionId) { this.questionId = questionId; }

    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }
}
