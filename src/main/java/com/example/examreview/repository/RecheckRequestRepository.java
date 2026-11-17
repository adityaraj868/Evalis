package com.example.examreview.repository;

import com.example.examreview.entity.RecheckRequest;
import com.example.examreview.entity.RequestStatus;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface RecheckRequestRepository extends JpaRepository<RecheckRequest, Long> {
    boolean existsByStudentIdAndExamIdAndQuestionId(Long studentId, Long examId, Long questionId);
    Optional<RecheckRequest> findByStudentIdAndExamIdAndQuestionId(Long studentId, Long examId, Long questionId);

    @EntityGraph(attributePaths = {"student", "exam", "question"})
    List<RecheckRequest> findByStudentIdOrderByCreatedAtDesc(Long studentId);

    @EntityGraph(attributePaths = {"student", "exam", "question"})
    List<RecheckRequest> findByExamIdOrderByCreatedAtDesc(Long examId);

    List<RecheckRequest> findByQuestionIdOrderByCreatedAtDesc(Long questionId);
    List<RecheckRequest> findByStatus(RequestStatus status);
    long countByQuestionId(Long questionId);
    long countByExamId(Long examId);

    @Query("SELECT r.question.id, COUNT(r) FROM RecheckRequest r WHERE r.exam.id = :examId GROUP BY r.question.id")
    List<Object[]> countRequestsByQuestionForExam(@Param("examId") Long examId);

    @Override
    @EntityGraph(attributePaths = {"student", "exam", "question"})
    List<RecheckRequest> findAll();

    @Override
    @EntityGraph(attributePaths = {"student", "exam", "question", "reviews"})
    Optional<RecheckRequest> findById(Long id);
}
