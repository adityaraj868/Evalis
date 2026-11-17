# Phase 6 — Request Tracking
## Exam Question Re-evaluation & Review Management System

**Phase Status**: `COMPLETED`  
**Execution Date**: November 18, 2026  
**Lead Architect**: Senior Software Architect & Lead Backend Engineer  

---

## 1. Objectives & Requirements

Phase 6 implements end-to-end request status tracking, lifecycle progression, and student feedback transparency:
- **Request Lifecycle Progression**:
  `SUBMITTED → UNDER_REVIEW → APPROVED / REJECTED`
- **Automatic Status Transition**: Requests in `SUBMITTED` state transition automatically to `UNDER_REVIEW` when a faculty evaluator opens the review workspace for that request.
- **Student Request Dashboard (`/student/requests`)**: Reverse chronological list of all filed rechecks with exam title, question target, submission timestamp, and badge status.
- **Individual Request Details (`/student/requests/{id}`)**: Full tracking view exposing original score, question ceiling, submitted justification, faculty review outcome, and revised marks.
- **Security & Data Isolation**:
  - Horizontal privilege escalation (IDOR) prevention: students can only access their own requests (`UnauthorizedAccessException` on mismatch).
  - Immutability: students cannot alter or tamper with faculty review decisions.
- **Audit Integration**: Logging `REQUEST_UNDER_REVIEW` events.

---

## 2. Architectural Design & Implementation

### 2.1 Request State Transition Model
- State transitions are strictly unidirectional:
  - `SUBMITTED`: Initial state upon student submission.
  - `UNDER_REVIEW`: Triggered automatically when faculty opens `/faculty/requests/{id}` via `recheckRequestService.markUnderReview(...)`.
  - `APPROVED` / `REJECTED`: Final terminal state set by faculty in Phase 7.
- Transition rules are enforced within `@Transactional` methods and logged to the audit repository.

### 2.2 Security & Ownership Isolation
In `StudentController.requestDetail`:
```java
RecheckRequest request = recheckRequestService.getRequestById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Re-evaluation request not found with ID: " + id));

if (!request.getStudent().getId().equals(currentUser.getId())) {
    throw new UnauthorizedAccessException("You are not authorized to view another student's re-evaluation request.");
}
```

### 2.3 User Interface
- **`templates/student/requests.html`**: Request list with ID, exam name, question number, formatted timestamp, status badge, and "Track & Details" action link.
- **`templates/student/request-detail.html`**: Visual timeline card showing submission details, current marks, question text, justification, and faculty outcome banner (with reviewer name, review timestamp, decision badge, revised marks, and evaluator comments).

---

## 3. Files Created & Modified

| File Path | Action | Description |
|---|---|---|
| `service/RecheckRequestService.java` | Modified | Added `markUnderReview(requestId, actor)` method with audit event logging. |
| `controller/FacultyController.java` | Modified | Integrated automatic transition to `UNDER_REVIEW` upon opening request. |
| `controller/StudentController.java` | Modified | Enforced student data ownership checks and clean 404/403 mapping. |
| `templates/student/requests.html` | Inspected & Verified | Verified UI layout, badges, and timestamps. |
| `templates/student/request-detail.html` | Inspected & Verified | Verified review outcome transparency and revised marks display. |
| `test/.../service/RequestTrackingTests.java` | Created | 4 automated tests verifying tracking history, `UNDER_REVIEW` transition, IDOR prevention, and review outcome visibility. |

---

## 4. Testing & Verification

Executed `RequestTrackingTests` via Maven Surefire:
1. `testStudentCanTrackOwnRequests`: Verified student retrieves requests in reverse chronological order with accurate timestamps.
2. `testRequestTransitionsToUnderReviewWhenOpenedByFaculty`: Verified automatic transition from `SUBMITTED` → `UNDER_REVIEW`.
3. `testStudentCannotAccessOtherStudentsRequest`: Verified IDOR protection isolating student records.
4. `testStudentCanSeeFacultyReviewOutcomeAndRevisedMarks`: Verified student visibility of faculty name, review comments, and revised scores.

**Test Results**: 4 tests run, 0 failures, 0 errors, 0 skipped.

---

## 5. Exit Criteria Verification

- [x] Students can track their re-evaluation requests from submission to final decision.
- [x] Unidirectional state progression `SUBMITTED` → `UNDER_REVIEW` → `APPROVED`/`REJECTED` is strictly maintained.
- [x] Cross-student access is blocked on the backend.
- [x] Automated test suite verified with 100% pass rate.
