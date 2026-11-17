# Phase 5 — Re-evaluation Request Core
## Exam Question Re-evaluation & Review Management System

**Phase Status**: `COMPLETED`  
**Execution Date**: November 18, 2026  
**Lead Architect**: Senior Software Architect & Lead Backend Engineer  

---

## 1. Objectives & Requirements

Phase 5 implements the core re-evaluation submission engine, enforcing academic eligibility, temporal windows, and multi-tier duplicate prevention:
- **Granular Question-Level Filing**: Students submit requests targeting specific disputed questions rather than entire exams.
- **Justification Validation**: Mandatory technical reasoning ($\ge 5$ characters).
- **Temporal Window Enforcement**: Validating `LocalDateTime` against `reevaluationStart` and `reevaluationEnd`. Submissions outside this window or on exams not in `RE_EVALUATION_OPEN` status are strictly rejected.
- **Eligibility Checks**: Verifying student has active enrollment/results on record and that question-level marks exist.
- **Multi-Tier Duplicate Prevention (ADR-003)**:
  - Application-level pre-check: `existsByStudentIdAndExamIdAndQuestionId(...)`.
  - Database-level unique constraint: `UNIQUE(student_id, exam_id, question_id)`.
  - Concurrency safety: Catching `DataIntegrityViolationException` and translating it into a domain-level `DuplicateRequestException`.
- **Audit Logging**: Capturing `REQUEST_SUBMITTED` events with actor, question ID, and timestamp.

---

## 2. Architectural Design & Implementation

### 2.1 Multi-Layer Validation Pipeline (`RecheckRequestService.java`)
Every request passes through an authoritative backend pipeline:
1. **Actor Verification**: Confirms caller is authenticated and possesses `ROLE_STUDENT`.
2. **Justification Check**: Rejects blank or trivial entries under 5 characters (`ValidationException`).
3. **Question & Exam Association**: Validates question exists and belongs to the specified `examId` (`ValidationException`).
4. **Lifecycle & Window Checks**:
   - `exam.getStatus() == ExamStatus.RE_EVALUATION_OPEN` (`InvalidStateTransitionException`).
   - `now.isBefore(exam.getReevaluationStart())` (`InvalidStateTransitionException`).
   - `now.isAfter(exam.getReevaluationEnd())` (`InvalidStateTransitionException`).
5. **Enrollment & Marks Check**:
   - Confirms `studentResultRepository.existsByStudentIdAndExamId(...)` (`UnauthorizedAccessException`).
   - Confirms `questionMarkRepository.existsByStudentIdAndQuestionId(...)` (`ValidationException`).
6. **Concurrency & Uniqueness Enforcement**:
   - Application check prevents redundant round-trips.
   - `saveAndFlush` triggers database unique constraint checks within the transactional boundary. Any race condition collision produces `DuplicateRequestException`.

### 2.2 DTO Integration (`RecheckRequestFormDto.java`)
- Binds `examId`, `questionId`, and `reason` with Jakarta bean validation (`@NotNull`, `@NotBlank`, `@Size(min = 5, max = 2000)`).

---

## 3. Files Created & Modified

| File Path | Action | Description |
|---|---|---|
| `service/RecheckRequestService.java` | Modified | Integrated domain exception hierarchy, window checks, eligibility checks, and concurrency handling. |
| `controller/StudentController.java` | Modified | Updated exception handling in `submitRequest` to catch domain exceptions and report flash messages. |
| `dto/RecheckRequestFormDto.java` | Created | DTO encapsulating recheck request submission data. |
| `test/.../service/RecheckRequestCoreTests.java` | Created | 9 unit/integration tests verifying submission validation, window boundaries, and duplicate rejection. |

---

## 4. Testing & Verification

Executed `RecheckRequestCoreTests` via Maven Surefire:
1. `testSubmitValidRequest`: Verified successful submission persisting `SUBMITTED` status and audit record.
2. `testSubmitRequestOutsideWindowFails`: Verified rejection when status is not `RE_EVALUATION_OPEN`.
3. `testSubmitRequestBeforeStartTimeFails`: Verified rejection before start timestamp.
4. `testSubmitRequestAfterEndTimeFails`: Verified rejection after closing timestamp.
5. `testSubmitRequestWithoutStudentEnrollmentFails`: Verified rejection for unenrolled students (`UnauthorizedAccessException`).
6. `testSubmitRequestWithoutQuestionMarksFails`: Verified rejection when no marks exist for the question.
7. `testSubmitRequestShortReasonFails`: Verified rejection of reasons under 5 characters.
8. `testDuplicateRequestPreventedAtApplicationLevel`: Verified second request triggers `DuplicateRequestException`.
9. `testNonStudentCannotSubmitRequest`: Verified non-students are blocked with `UnauthorizedAccessException`.

**Test Results**: 9 tests run, 0 failures, 0 errors, 0 skipped.

---

## 5. Exit Criteria Verification

- [x] Students can submit valid re-evaluation requests for eligible questions.
- [x] Submissions outside temporal windows are safely rejected.
- [x] Database-level unique constraint `UNIQUE(student_id, exam_id, question_id)` guarantees duplicate prevention under concurrency.
- [x] All 9 automated tests passed without errors.
