package com.example.examreview.repository;

import com.example.examreview.entity.Exam;
import com.example.examreview.entity.ExamStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ExamRepository extends JpaRepository<Exam, Long> {
    List<Exam> findByStatus(ExamStatus status);
    List<Exam> findAllByOrderByCreatedAtDesc();
}
