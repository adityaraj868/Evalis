# Phase 7 — Faculty Review Workflow
## Exam Question Re-evaluation & Review Management System

**Phase Status**: `COMPLETED`  
**Execution Date**: November 18, 2026  
**Lead Architect**: Senior Software Architect & Lead Backend Engineer  

---

## 1. Objectives & Requirements

Phase 7 implements the authoritative faculty decision-making and mark amendment workflow:
- **Faculty Review Workspace (`/faculty/requests/{id}`)**: Detailed claim view with question context, current mark, student-submitted justification, and decision form.
- **Decision Processing**: Supporting `APPROVED` and `REJECTED` decisions with mandatory evaluator comments.
- **Score Amendment**: When `APPROVED`, revised marks are validated against question limits ($0.0 \le \text{revisedMarks} \le \text{maxMarks}$).
- **Automatic Recalculation**: Transactional score update in `question_marks` and arithmetic synchronization in `student_results`.
- **Integrity Guards**:
  - Rejection does not modify student marks.
  - Finalized decisions (`APPROVED` or `REJECTED`) are immutable; subsequent review attempts trigger `InvalidStateTransitionException`.
  - Only users with `ROLE_FACULTY` or `ROLE_ADMIN` can execute reviews (`UnauthorizedAccessException` on unauthorized callers).
- **Audit Logging**: Comprehensive recording of `REVIEW_COMPLETED` events.

---

## 2. Architectural Design & Implementation

### 2.1 The 8-Step Review Execution Pipeline (`ReviewService.java`)
1. **Caller Verification**: Validates caller holds `ROLE_FACULTY` or `ROLE_ADMIN`.
2. **Request Resolution**: Fetches target request or throws `ResourceNotFoundException`.
3. **State Immutability Guard**: Validates request has not already received a final decision (`APPROVED` or `REJECTED`).
4. **Bounds & Parameter Validation**:
   - For `APPROVED`: enforces `revisedMarks != null`, `revisedMarks >= 0.0`, and `revisedMarks <= question.getMaxMarks()`.
   - For `REJECTED`: ensures marks remain unaltered.
5. **Review Record Persistence**: Persists a new `Review` entity containing decision, comments, revised marks, timestamp, and reviewer ID.
6. **Request Status Update**: Transitions request status to `APPROVED` or `REJECTED`.
7. **Transactional Mark Synchronization**: Calls `marksService.updateMarksAfterReview(...)`, atomically modifying `QuestionMark` and recalculating `StudentResult.totalMarks`.
8. **Audit Trail Logging**: Dispatches `REVIEW_COMPLETED` audit log entry.

### 2.2 DTO Integration (`ReviewFormDto.java`)
- Captures `ReviewDecision`, `revisedMarks`, and `comments` with validation constraints.

---

## 3. Files Created & Modified

| File Path | Action | Description |
|---|---|---|
| `service/ReviewService.java` | Modified | Implemented full review processing, state validation, bounds checks, transactional score revision, and audit logging. |
| `controller/FacultyController.java` | Modified | Updated `submitReview` endpoint with exception translation and flash message handling. |
| `dto/ReviewFormDto.java` | Created | DTO encapsulating faculty review input. |
| `templates/faculty/request-review.html` | Inspected & Verified | Verified interactive radio toggling of revised marks input and validation feedback. |
| `test/.../service/FacultyReviewWorkflowTests.java` | Created | 7 automated tests covering approval, rejection, mark bounds validation, immutability, and security. |

---

## 4. Testing & Verification

Executed `FacultyReviewWorkflowTests` via Maven Surefire:
1. `testApproveRequestUpdatesMarksAndRecalculatesTotal`: Verified approval updates question mark, recalculates total score, and updates request status.
2. `testRejectRequestMaintainsOriginalMarks`: Verified rejection leaves original marks untouched.
3. `testApproveRequestWithMissingMarksFails`: Verified missing revised marks triggers `ValidationException`.
4. `testApproveRequestWithNegativeMarksFails`: Verified negative revised marks trigger `ValidationException`.
5. `testApproveRequestExceedingMaxMarksFails`: Verified revised marks > maxMarks trigger `ValidationException`.
6. `testCannotReviewAlreadyDecidedRequest`: Verified attempts to re-review decided requests trigger `InvalidStateTransitionException`.
7. `testNonFacultyCannotReviewRequest`: Verified unauthorized callers trigger `UnauthorizedAccessException`.

**Test Results**: 7 tests run, 0 failures, 0 errors, 0 skipped.

---

## 5. Exit Criteria Verification

- [x] Faculty can review pending requests with student-provided justification.
- [x] Approved mark revisions update student examination results atomically.
- [x] Rejected requests maintain original marks.
- [x] Immutability prevents duplicate or conflicting decisions on finalized requests.
- [x] All 7 automated tests passed with 100% success rate.
