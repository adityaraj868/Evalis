package com.example.examreview.repository;

import com.example.examreview.entity.QuestionMark;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface QuestionMarkRepository extends JpaRepository<QuestionMark, Long> {
    Optional<QuestionMark> findByStudentIdAndQuestionId(Long studentId, Long questionId);
    List<QuestionMark> findByStudentId(Long studentId);
    List<QuestionMark> findByQuestionExamIdAndStudentId(Long examId, Long studentId);
    boolean existsByStudentIdAndQuestionId(Long studentId, Long questionId);
}
