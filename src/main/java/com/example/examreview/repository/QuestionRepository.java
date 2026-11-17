package com.example.examreview.repository;

import com.example.examreview.entity.Question;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface QuestionRepository extends JpaRepository<Question, Long> {
    List<Question> findByExamIdOrderByQuestionNumberAsc(Long examId);
    List<Question> findByExamId(Long examId);
}
