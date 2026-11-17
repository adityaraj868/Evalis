package com.example.examreview.repository;

import com.example.examreview.entity.StudentResult;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StudentResultRepository extends JpaRepository<StudentResult, Long> {
    Optional<StudentResult> findByStudentIdAndExamId(Long studentId, Long examId);

    @EntityGraph(attributePaths = {"exam", "student"})
    List<StudentResult> findByStudentId(Long studentId);

    @EntityGraph(attributePaths = {"exam", "student"})
    List<StudentResult> findByExamId(Long examId);

    boolean existsByStudentIdAndExamId(Long studentId, Long examId);
}
