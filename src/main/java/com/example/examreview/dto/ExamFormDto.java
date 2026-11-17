package com.example.examreview.dto;

import com.example.examreview.entity.ExamStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDate;

public class ExamFormDto {

    private Long id;

    @NotBlank(message = "Examination name is required.")
    @Size(max = 150, message = "Examination name must not exceed 150 characters.")
    private String name;

    @NotBlank(message = "Subject is required.")
    @Size(max = 100, message = "Subject must not exceed 100 characters.")
    private String subject;

    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
    private LocalDate startDate;

    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
    private LocalDate endDate;

    private ExamStatus status = ExamStatus.DRAFT;

    public ExamFormDto() {}

    public ExamFormDto(Long id, String name, String subject, LocalDate startDate, LocalDate endDate, ExamStatus status) {
        this.id = id;
        this.name = name;
        this.subject = subject;
        this.startDate = startDate;
        this.endDate = endDate;
        this.status = status;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getSubject() { return subject; }
    public void setSubject(String subject) { this.subject = subject; }

    public LocalDate getStartDate() { return startDate; }
    public void setStartDate(LocalDate startDate) { this.startDate = startDate; }

    public LocalDate getEndDate() { return endDate; }
    public void setEndDate(LocalDate endDate) { this.endDate = endDate; }

    public ExamStatus getStatus() { return status; }
    public void setStatus(ExamStatus status) { this.status = status; }
}
