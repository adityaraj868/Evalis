package com.example.examreview.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "reviews", indexes = {
    @Index(name = "idx_reviews_request_id", columnList = "request_id"),
    @Index(name = "idx_reviews_faculty_id", columnList = "faculty_id")
})
public class Review {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "request_id", nullable = false)
    private RecheckRequest request;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "faculty_id", nullable = false)
    private User faculty;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private ReviewDecision decision;

    @Column(columnDefinition = "TEXT")
    private String comments;

    @Column(name = "revised_marks")
    private Double revisedMarks;

    @Column(name = "reviewed_at", nullable = false)
    private LocalDateTime reviewedAt;

    public Review() {
    }

    public Review(RecheckRequest request, User faculty, ReviewDecision decision, String comments, Double revisedMarks) {
        this.request = request;
        this.faculty = faculty;
        this.decision = decision;
        this.comments = comments;
        this.revisedMarks = revisedMarks;
    }

    @PrePersist
    protected void onCreate() {
        if (this.reviewedAt == null) {
            this.reviewedAt = LocalDateTime.now();
        }
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public RecheckRequest getRequest() {
        return request;
    }

    public void setRequest(RecheckRequest request) {
        this.request = request;
    }

    public User getFaculty() {
        return faculty;
    }

    public void setFaculty(User faculty) {
        this.faculty = faculty;
    }

    public ReviewDecision getDecision() {
        return decision;
    }

    public void setDecision(ReviewDecision decision) {
        this.decision = decision;
    }

    public String getComments() {
        return comments;
    }

    public void setComments(String comments) {
        this.comments = comments;
    }

    public Double getRevisedMarks() {
        return revisedMarks;
    }

    public void setRevisedMarks(Double revisedMarks) {
        this.revisedMarks = revisedMarks;
    }

    public LocalDateTime getReviewedAt() {
        return reviewedAt;
    }

    public void setReviewedAt(LocalDateTime reviewedAt) {
        this.reviewedAt = reviewedAt;
    }
}
