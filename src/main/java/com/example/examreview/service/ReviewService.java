package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.repository.RecheckRequestRepository;
import com.example.examreview.repository.ReviewRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ReviewService {

    private final ReviewRepository reviewRepository;
    private final RecheckRequestRepository recheckRequestRepository;
    private final MarksService marksService;
    private final AuditService auditService;

    public ReviewService(ReviewRepository reviewRepository,
                         RecheckRequestRepository recheckRequestRepository,
                         MarksService marksService,
                         AuditService auditService) {
        this.reviewRepository = reviewRepository;
        this.recheckRequestRepository = recheckRequestRepository;
        this.marksService = marksService;
        this.auditService = auditService;
    }

    @Transactional
    public Review processReview(Long requestId, User faculty, ReviewDecision decision, String comments, Double revisedMarks) {
        RecheckRequest request = recheckRequestRepository.findById(requestId)
                .orElseThrow(() -> new IllegalArgumentException("Request not found: " + requestId));

        if (decision == ReviewDecision.APPROVED) {
            if (revisedMarks == null) {
                throw new IllegalArgumentException("Revised marks must be provided when approving a request.");
            }
            if (revisedMarks < 0) {
                throw new IllegalArgumentException("Revised marks cannot be negative.");
            }
            Double maxMarks = request.getQuestion().getMaxMarks();
            if (revisedMarks > maxMarks) {
                throw new IllegalArgumentException("Revised marks (" + revisedMarks + ") cannot exceed maximum question marks (" + maxMarks + ").");
            }
        }

        Review review = new Review(request, faculty, decision, comments, revisedMarks);
        review.setReviewedAt(LocalDateTime.now());
        Review savedReview = reviewRepository.save(review);

        // Update Request status
        if (decision == ReviewDecision.APPROVED) {
            request.setStatus(RequestStatus.APPROVED);
            // Update the question mark and total student result
            marksService.updateMarksAfterReview(request.getStudent().getId(), request.getQuestion().getId(), revisedMarks, faculty);
        } else {
            request.setStatus(RequestStatus.REJECTED);
        }
        recheckRequestRepository.save(request);

        auditService.log(faculty, "REVIEW_COMPLETED",
                String.format("Faculty %s %s request ID %d for question %d. Comments: %s",
                        faculty.getName(), decision, requestId, request.getQuestion().getQuestionNumber(),
                        comments != null ? comments : "None"));

        return savedReview;
    }

    public List<Review> getReviewsForRequest(Long requestId) {
        return reviewRepository.findByRequestIdOrderByReviewedAtDesc(requestId);
    }
}
