# Phase 4 — Marks Management
## Exam Question Re-evaluation & Review Management System

**Phase Status**: `COMPLETED`  
**Execution Date**: November 18, 2026  
**Lead Architect**: Senior Software Architect & Lead Backend Engineer  

---

## 1. Objectives & Requirements

Phase 4 implements granular question-level marks recording, student examination marksheets, and transactional total calculations:
- **Question-Level Marks Recording**: Storing individual scores in `question_marks` table with `UNIQUE(student_id, question_id)`.
- **Bounds Validation**: Enforcing `0.0 <= marksObtained <= maxMarks` strictly on the backend. Negative marks or marks exceeding ceilings trigger `ValidationException`.
- **Automatic Total Calculation**: Recalculating and synchronizing `StudentResult.totalMarks` whenever any individual question mark is created or revised.
- **Faculty Marks Management Interface**: Web views allowing faculty to inspect student marksheets and record question marks for all enrolled candidates.
- **Atomic Transactions**: `@Transactional` boundaries guaranteeing that question-level marks and exam totals update consistently without partial failure.
- **Audit Integration**: Logging `MARK_RECORDED`, `STUDENT_MARKS_RECORDED`, and `MARKS_REVISED` events.

---

## 2. Architectural Design & Implementation

### 2.1 Marks Calculation & Synchronization (`MarksService.java`)
Whenever a mark is entered or amended:
1. Bounds validation is executed: `validateMarkBounds(Question, marksObtained)`.
2. Existing mark is fetched or new `QuestionMark` instantiated.
3. `recalculateStudentResult(student, exam)` queries all question marks for that student in that exam, calculates the arithmetic sum, and updates `StudentResult`.
4. The entire operation runs within a Spring `@Transactional` context, ensuring full ACID guarantees.

### 2.2 Key Methods Implemented in `MarksService`
- `recordMark(User student, Question question, Double marksObtained, User actor)`: Records a mark for an individual question with bounds validation, role verification, and audit trail logging.
- `recordExamMarksForStudent(Long examId, Long studentId, Map<Long, Double> questionMarks, User actor)`: Atomic batch marks recording across all examination questions for a student, returning the updated `StudentResult`.
- `updateMarksAfterReview(Long studentId, Long questionId, Double revisedMarks, User faculty)`: Updates score after faculty review approval and triggers total result recalculation.
- `getExamResults(Long examId)`: Retrieves all student results for an exam.

### 2.3 User Interface
- **`templates/faculty/exam-marks.html`**: Enrolled students table with recorded/pending status badges and direct access to enter/edit marks.
- **`templates/faculty/student-marks-edit.html`**: Question-by-question input form with real-time max marks constraints and prefilled existing scores.
- **`templates/faculty/exams.html`**: Added "Marks" action link for quick access.

---

## 3. Files Created & Modified

| File Path | Action | Description |
|---|---|---|
| `service/MarksService.java` | Modified | Added batch marks recording, bounds validation, audit events, and security assertions. |
| `controller/FacultyController.java` | Modified | Added `/exams/{id}/marks` and `/exams/{id}/marks/student/{studentId}` GET/POST endpoints. |
| `dto/MarksEntryDto.java` | Created | DTO encapsulating question-to-marks mapping. |
| `templates/faculty/exam-marks.html` | Created | Faculty examination marksheet dashboard. |
| `templates/faculty/student-marks-edit.html` | Created | Question-level marks entry and editing template. |
| `templates/faculty/exams.html` | Modified | Added "Marks" action button. |
| `test/.../service/MarksManagementTests.java` | Created | 6 automated tests verifying marks bounds, batch entry, total recalculation, and security. |

---

## 4. Testing & Verification

Executed `MarksManagementTests` via Maven Surefire:
1. `testRecordMarkSuccess`: Verified mark recording on single question and automatic `StudentResult.totalMarks` synchronization.
2. `testRecordMarkNegativeThrowsValidationException`: Verified negative marks are rejected with `ValidationException`.
3. `testRecordMarkExceedingMaxMarksThrowsValidationException`: Verified marks > maxMarks are rejected with `ValidationException`.
4. `testRecordExamMarksForStudentBatch`: Verified multi-question batch recording and total sum calculation (`9.0 + 14.0 + 12.5 = 35.5`).
5. `testUpdateMarksAfterReviewRecalculatesTotal`: Verified that revising a question mark from 6.0 to 9.0 recalculates total from 16.0 to 19.0 atomically.
6. `testNonFacultyCannotRecordMarks`: Verified students cannot record marks (`UnauthorizedAccessException`).

**Test Results**: 6 tests run, 0 failures, 0 errors, 0 skipped.

---

## 5. Exit Criteria Verification

- [x] Faculty can record and edit marks at the question level.
- [x] Students can view accurate breakdown and total examination results.
- [x] Maximum marks ceilings are strictly enforced.
- [x] All database transactions maintain total and question-level consistency.
- [x] Automated test suite verified with 100% pass rate.
