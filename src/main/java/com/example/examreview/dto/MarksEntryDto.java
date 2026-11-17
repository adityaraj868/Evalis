package com.example.examreview.dto;

import java.util.HashMap;
import java.util.Map;

public class MarksEntryDto {

    private Long examId;
    private Long studentId;
    private Map<Long, Double> questionMarks = new HashMap<>();

    public MarksEntryDto() {}

    public MarksEntryDto(Long examId, Long studentId) {
        this.examId = examId;
        this.studentId = studentId;
    }

    public Long getExamId() { return examId; }
    public void setExamId(Long examId) { this.examId = examId; }

    public Long getStudentId() { return studentId; }
    public void setStudentId(Long studentId) { this.studentId = studentId; }

    public Map<Long, Double> getQuestionMarks() { return questionMarks; }
    public void setQuestionMarks(Map<Long, Double> questionMarks) { this.questionMarks = questionMarks; }
}
