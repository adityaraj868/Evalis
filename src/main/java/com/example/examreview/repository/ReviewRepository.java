package com.example.examreview.repository;

import com.example.examreview.entity.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByRequestIdOrderByReviewedAtDesc(Long requestId);
    List<Review> findByFacultyIdOrderByReviewedAtDesc(Long facultyId);
}
