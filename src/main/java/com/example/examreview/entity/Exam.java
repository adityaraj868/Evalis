package com.example.examreview.entity;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "exams", indexes = {
    @Index(name = "idx_exams_status", columnList = "status"),
    @Index(name = "idx_exams_start_date", columnList = "start_date"),
    @Index(name = "idx_exams_end_date", columnList = "end_date")
})
public class Exam {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 150)
    private String name;

    @Column(nullable = false, length = 100)
    private String subject;

    @Column(name = "start_date")
    private LocalDate startDate;

    @Column(name = "end_date")
    private LocalDate endDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    private ExamStatus status = ExamStatus.DRAFT;

    @Column(name = "reevaluation_start")
    private LocalDateTime reevaluationStart;

    @Column(name = "reevaluation_end")
    private LocalDateTime reevaluationEnd;

    @OneToMany(mappedBy = "exam", cascade = CascadeType.ALL, orphanRemoval = true)
    @OrderBy("questionNumber ASC")
    private List<Question> questions = new ArrayList<>();

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    public Exam() {
    }

    public Exam(String name, String subject, LocalDate startDate, LocalDate endDate) {
        this.name = name;
        this.subject = subject;
        this.startDate = startDate;
        this.endDate = endDate;
        this.status = ExamStatus.DRAFT;
    }

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    public void addQuestion(Question question) {
        questions.add(question);
        question.setExam(this);
    }

    public void removeQuestion(Question question) {
        questions.remove(question);
        question.setExam(null);
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSubject() {
        return subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public void setStartDate(LocalDate startDate) {
        this.startDate = startDate;
    }

    public LocalDate getEndDate() {
        return endDate;
    }

    public void setEndDate(LocalDate endDate) {
        this.endDate = endDate;
    }

    public ExamStatus getStatus() {
        return status;
    }

    public void setStatus(ExamStatus status) {
        this.status = status;
    }

    public LocalDateTime getReevaluationStart() {
        return reevaluationStart;
    }

    public void setReevaluationStart(LocalDateTime reevaluationStart) {
        this.reevaluationStart = reevaluationStart;
    }

    public LocalDateTime getReevaluationEnd() {
        return reevaluationEnd;
    }

    public void setReevaluationEnd(LocalDateTime reevaluationEnd) {
        this.reevaluationEnd = reevaluationEnd;
    }

    public List<Question> getQuestions() {
        return questions;
    }

    public void setQuestions(List<Question> questions) {
        this.questions = questions;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}
