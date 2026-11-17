package com.example.examreview.service;

import com.example.examreview.entity.*;
import com.example.examreview.exception.InvalidStateTransitionException;
import com.example.examreview.exception.ResourceNotFoundException;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.exception.ValidationException;
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
        if (faculty == null || (faculty.getRole() != Role.FACULTY && faculty.getRole() != Role.ADMIN)) {
            throw new UnauthorizedAccessException("Only faculty members or administrators can review re-evaluation requests.");
        }

        RecheckRequest request = recheckRequestRepository.findById(requestId)
                .orElseThrow(() -> new ResourceNotFoundException("Re-evaluation request not found with ID: " + requestId));

        if (decision == null) {
            throw new ValidationException("A review decision (APPROVED or REJECTED) is required.");
        }

        // Prevent modifying already decided requests
        if (request.getStatus() == RequestStatus.APPROVED || request.getStatus() == RequestStatus.REJECTED) {
            throw new InvalidStateTransitionException("This re-evaluation request has already received a final decision (" + request.getStatus() + ").");
        }

        if (decision == ReviewDecision.APPROVED) {
            if (revisedMarks == null) {
                throw new ValidationException("Revised marks must be provided when approving a re-evaluation request.");
            }
            if (revisedMarks < 0.0) {
                throw new ValidationException("Revised marks cannot be negative.");
            }
            Double maxMarks = request.getQuestion().getMaxMarks();
            if (maxMarks != null && revisedMarks > maxMarks) {
                throw new ValidationException(String.format("Revised marks (%.1f) cannot exceed maximum question marks (%.1f).",
                        revisedMarks, maxMarks));
            }
        }

        Review review = new Review(request, faculty, decision, comments != null ? comments.trim() : null, revisedMarks);
        review.setReviewedAt(LocalDateTime.now());
        Review savedReview = reviewRepository.save(review);

        // Update Request status and recalculate marks atomically
        if (decision == ReviewDecision.APPROVED) {
            request.setStatus(RequestStatus.APPROVED);
            marksService.updateMarksAfterReview(request.getStudent().getId(), request.getQuestion().getId(), revisedMarks, faculty);
        } else {
            request.setStatus(RequestStatus.REJECTED);
        }
        recheckRequestRepository.save(request);

        auditService.log(faculty, "REVIEW_COMPLETED",
                String.format("Faculty %s %s request ID %d for question %d. Revised marks: %s. Comments: %s",
                        faculty.getName(), decision, requestId, request.getQuestion().getQuestionNumber(),
                        revisedMarks != null ? String.valueOf(revisedMarks) : "N/A",
                        comments != null ? comments : "None"));

        return savedReview;
    }

    public List<Review> getReviewsForRequest(Long requestId) {
        return reviewRepository.findByRequestIdOrderByReviewedAtDesc(requestId);
    }

    public List<Review> getReviewsByFaculty(Long facultyId) {
        return reviewRepository.findByFacultyIdOrderByReviewedAtDesc(facultyId);
    }
}
