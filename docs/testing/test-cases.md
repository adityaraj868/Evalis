# Test Cases Specification
## Exam Question Re-evaluation & Review Management System

The automated test suite contains **67 tests** across **11 test classes**. Below is the test case specification.

---

### 1. Security & Access Control Suite (`SecurityAccessTests.java` - 8 Tests)

| Test ID | Test Method Name | Scenario / Preconditions | Expected Outcome |
|---|---|---|---|
| SEC-01 | `testUnauthenticatedAccessRedirectsToLogin` | Unauthenticated user requests `/student/dashboard` | HTTP 302 Redirect to `/login` |
| SEC-02 | `testStudentAccessToFacultyRouteForbidden` | User with `ROLE_STUDENT` requests `/faculty/dashboard` | HTTP 403 Forbidden |
| SEC-03 | `testFacultyAccessToAdminRouteForbidden` | User with `ROLE_FACULTY` requests `/admin/audit-logs` | HTTP 403 Forbidden |
| SEC-04 | `testAdminCanAccessAdminDashboard` | User with `ROLE_ADMIN` requests `/admin/dashboard` | HTTP 200 OK |
| SEC-05 | `testValidLoginRedirects` | Post valid credentials to `/login` with `ROLE_STUDENT` | HTTP 302 Redirect to `/student/dashboard` |
| SEC-06 | `testInvalidLoginRedirectsWithError` | Post invalid credentials to `/login` | HTTP 302 Redirect to `/login?error=true` |
| SEC-07 | `testStudentCannotViewAnotherStudentsRequest` | Student A requests `/student/requests/{id}` belonging to Student B | HTTP 403 Forbidden (Anti-IDOR) |
| SEC-08 | `testStudentCanViewOwnRequest` | Student A requests `/student/requests/{id}` belonging to Student A | HTTP 200 OK |

---

### 2. Examination Lifecycle Suite (`ExamLifecycleTests.java` - 11 Tests)

| Test ID | Test Method Name | Scenario | Expected Outcome |
|---|---|---|---|
| EXM-01 | `testCreateExamSuccess` | Valid exam parameters in DRAFT | Exam created with status `DRAFT` |
| EXM-02 | `testPublishExamWithQuestions` | Exam has 1 question; faculty triggers publish | Status transitions to `PUBLISHED` |
| EXM-03 | `testPublishExamWithoutQuestionsFails` | Exam has 0 questions; faculty triggers publish | Throws `ValidationException` |
| EXM-04 | `testCannotAddQuestionsAfterPublished` | Exam is `PUBLISHED`; faculty attempts to add question | Throws `InvalidStateTransitionException` |
| EXM-05 | `testOpenReevaluationWindow` | Exam is `PUBLISHED`; faculty opens re-evaluation window | Status transitions to `RE_EVALUATION_OPEN` |
| EXM-06 | `testCloseReevaluationWindow` | Exam is `RE_EVALUATION_OPEN`; faculty closes window | Status transitions to `RE_EVALUATION_CLOSED` |
| EXM-07 | `testArchiveExam` | Exam is `RE_EVALUATION_CLOSED`; faculty archives exam | Status transitions to `ARCHIVED` |
| EXM-08 | `testInvalidStateTransitionThrowsException` | Attempting to transition `DRAFT` directly to `ARCHIVED` | Throws `InvalidStateTransitionException` |
| EXM-09 | `testExamTitleTooShortFails` | Creating exam with 1-character title | Throws `ValidationException` |
| EXM-10 | `testQuestionMaxMarksZeroFails` | Adding question with $maxMarks = 0.0$ | Throws `ValidationException` |
| EXM-11 | `testUpdateExamInDraftStatus` | Modifying name and dates while in `DRAFT` | Updates applied successfully |

---

### 3. Marks Management Suite (`MarksManagementTests.java` - 6 Tests)

| Test ID | Test Method Name | Scenario | Expected Outcome |
|---|---|---|---|
| MRK-01 | `testRecordExamMarksSuccess` | Batch recording valid marks for student | Marks saved, `totalMarks` recalculated correctly |
| MRK-02 | `testNegativeMarksThrowsException` | Recording mark with score $< 0.0$ | Throws `ValidationException` |
| MRK-03 | `testMarksExceedingMaxMarksThrowsException` | Recording score $> maxMarks$ | Throws `ValidationException` |
| MRK-04 | `testBatchMarksUpdateRecalculatesTotal` | Modifying existing marks | `StudentResult.totalMarks` updated to match new sum |
| MRK-05 | `testMarksAuditLogging` | Recording marks | Audit log emitted with action `MARKS_RECORDED` |
| MRK-06 | `testUnenrolledStudentMarksThrowsException`| Recording marks for non-existent student | Throws `ResourceNotFoundException` |

---

### 4. Re-evaluation Request Suite (`RecheckRequestCoreTests.java` - 9 Tests)

| Test ID | Test Method Name | Scenario | Expected Outcome |
|---|---|---|---|
| REQ-01 | `testSubmitRecheckRequestSuccess` | Valid submission inside active window | Request created in `SUBMITTED` status |
| REQ-02 | `testDuplicateRequestThrowsException` | Duplicate submission for same question | Throws `DuplicateRequestException` |
| REQ-03 | `testReasonTooShortThrowsException` | Reason $< 5$ characters | Throws `ValidationException` |
| REQ-04 | `testSubmitWhenExamNotOpenFails` | Submitting when exam is in `DRAFT` or `PUBLISHED` | Throws `InvalidStateTransitionException` |
| REQ-05 | `testSubmitOutsideTimeWindowFails` | Current time is past `reevaluationEnd` | Throws `InvalidStateTransitionException` |
| REQ-06 | `testQuestionNotBelongingToExamFails` | Submitting question ID from a different exam | Throws `ValidationException` |
| REQ-07 | `testStudentWithoutQuestionMarkFails` | Submitting request for question with no mark recorded | Throws `ValidationException` |
| REQ-08 | `testDatabaseConstraintCatchesDuplicate` | Bypassing app check directly to repository | `DataIntegrityViolationException` caught |
| REQ-09 | `testAuditLogRecordedOnSubmission` | Successful submission | Audit log emitted with action `REQUEST_SUBMITTED` |

---

### 5. Request Tracking Suite (`RequestTrackingTests.java` - 4 Tests)

| Test ID | Test Method Name | Scenario | Expected Outcome |
|---|---|---|---|
| TRK-01 | `testMarkUnderReviewOnFacultyOpen` | Faculty opens request details | Request transitions `SUBMITTED` $\rightarrow$ `UNDER_REVIEW` |
| TRK-02 | `testMarkUnderReviewAuditLog` | Transition to `UNDER_REVIEW` | Audit log emitted with action `REQUEST_UNDER_REVIEW` |
| TRK-03 | `testStudentCanTrackRequestStatus` | Student queries list of their own requests | Returns list matching current statuses |
| TRK-04 | `testNonExistentRequestThrowsException` | Fetching invalid request ID | Throws `ResourceNotFoundException` |

---

### 6. Faculty Review Workflow Suite (`FacultyReviewWorkflowTests.java` - 7 Tests)

| Test ID | Test Method Name | Scenario | Expected Outcome |
|---|---|---|---|
| REV-01 | `testApproveReviewUpdatesMarksAndTotal` | Faculty approves with increased mark | Question mark updated, `StudentResult` recalculated |
| REV-02 | `testRejectReviewLeavesMarksUntouched` | Faculty rejects request | Request `REJECTED`, marks remain original value |
| REV-03 | `testReviewDecisionIsImmutable` | Attempting to review an already-approved request | Throws `InvalidStateTransitionException` |
| REV-04 | `testRevisedMarksExceedingMaxFails` | Approving with revised mark $> maxMarks$ | Throws `ValidationException` |
| REV-05 | `testEmptyCommentsThrowsException` | Submitting review without comments | Throws `ValidationException` |
| REV-06 | `testAuditLogEmittedOnReview` | Completing review | Audit log emitted with action `REVIEW_COMPLETED` |
| REV-07 | `testReviewWithNegativeMarksFails` | Approving with negative revised mark | Throws `ValidationException` |

---

### 7. Question-wise Analytics Suite (`QuestionAnalyticsTests.java` - 5 Tests)

| Test ID | Test Method Name | Scenario | Expected Outcome |
|---|---|---|---|
| ANL-01 | `testQuestionDisputeRateCalculation` | 10 students, 2 submit requests for Question 1 | Dispute rate computed as 20.0% |
| ANL-02 | `testDisputeThresholdFlagging` | Question dispute rate (25%) exceeds threshold (15%) | `isHighDispute` flag is `true` |
| ANL-03 | `testDivideByZeroProtection` | Exam with 0 enrolled students | Dispute rate returns 0.0%, no arithmetic error |
| ANL-04 | `testExamAnalyticsSummary` | Aggregate stats across 3 questions | Correct total requests, approved counts computed |
| ANL-05 | `testSingleQueryDisputeAggregation`| Single database query executed for counts | Repository returns aggregated pairs efficiently |

---

### 8. Centralized Audit Trail Suite (`AuditTrailTests.java` - 5 Tests)

| Test ID | Test Method Name | Scenario | Expected Outcome |
|---|---|---|---|
| AUD-01 | `testStructuredAuditLogEntry` | Logging event with action, resource, differentials | All columns correctly persisted and retrieved |
| AUD-02 | `testFilterAuditLogsByAction` | Filtering audit logs by action `REVIEW_COMPLETED` | Returns only matching log entries |
| AUD-03 | `testFilterAuditLogsByResourceType`| Filtering audit logs by resource `RecheckRequest` | Returns only matching resource entries |
| AUD-04 | `testFilterAuditLogsByUser` | Filtering audit logs by specific user ID | Returns only logs triggered by that user |
| AUD-05 | `testEntityGraphPreventsNPlusOne` | Fetching audit logs with associated users | Single SQL join executed via `@EntityGraph` |

---

### 9. Supporting Suites (12 Tests across 3 Classes)
- `DomainRepositoryTests.java` (8 Tests): Repository CRUD, constraints, cascading deletion.
- `HomeControllerSmokeTest.java` (3 Tests): Landing page rendering, unauthenticated routing.
- `ExamReviewApplicationTests.java` (1 Test): Spring Boot context initialization sanity check.
