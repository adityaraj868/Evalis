# Phase 8 — Question-wise Analytics
## Exam Question Re-evaluation & Review Management System

**Phase Status**: `COMPLETED`  
**Execution Date**: November 18, 2026  
**Lead Architect**: Senior Software Architect & Lead Backend Engineer  

---

## 1. Objectives & Requirements

Phase 8 implements real-time statistical aggregation and dispute diagnostic analytics for academic evaluators:
- **Dispute Frequency Aggregation**: Grouping student re-evaluation requests by question to pinpoint anomalous patterns.
- **Configurable Threshold Flagging**: Marking questions where dispute percentage exceeds a custom threshold (default 30%, user-adjustable from 1% to 100%).
- **Examination Metrics Breakdown**:
  - Total requests submitted for the examination.
  - Pending review count (`SUBMITTED` + `UNDER_REVIEW`).
  - Approved requests count.
  - Rejected requests count.
  - Enrolled cohort size.
- **Single-Query Efficiency**: Leveraging SQL aggregation (`COUNT(r) ... GROUP BY r.question.id`) to avoid $N+1$ query overhead.
- **Defensive Math**: Gracefully handling empty datasets or zero-cohort scenarios without divide-by-zero errors.
- **Role Isolation**: Restricting analytics access to `FACULTY` and `ADMIN` users.

---

## 2. Architectural Design & Implementation

### 2.1 Dedicated Analytics Service (`AnalyticsService.java`)
Separated business analytics from controller logic into a dedicated service:
1. `getExamAnalytics(Long examId, int threshold, User actor)`:
   - Validates caller role (`FACULTY` or `ADMIN`).
   - Fetches actual enrolled cohort count from `studentResultRepository.findByExamId(examId)`.
   - Fetches request status counts (`totalRequests`, `pendingRequests`, `approvedRequests`, `rejectedRequests`).
   - Executes aggregated group-by query via `recheckRequestRepository.countRequestsByQuestionForExam(examId)`.
   - Computes $\text{disputePercentage} = \frac{\text{requestCount}}{\text{cohortSize}} \times 100.0$.
   - Flags questions where $\text{disputePercentage} \ge \text{threshold}$.
   - Packages results in `ExamAnalyticsDto`.
2. `getHighDisputeQuestions(Long examId, int threshold, User actor)`:
   - Returns filtered list of flagged question analytics objects.

### 2.2 Data Transfer Objects
- **`QuestionAnalyticsDto`**: Encapsulates question entity, raw request count, dispute percentage, and boolean `flagged` status.
- **`ExamAnalyticsDto`**: Summarizes exam-level metrics and holds the list of `QuestionAnalyticsDto`.

### 2.3 User Interface
- **`templates/faculty/analytics.html`**:
  - Dropdown selector for active examinations.
  - Number input for dynamic flagging threshold adjustment.
  - Visual heatmap styling highlighting flagged questions in red with `⚠️ High Demand` badge and "Inspect" button linking to filtered requests.

---

## 3. Files Created & Modified

| File Path | Action | Description |
|---|---|---|
| `service/AnalyticsService.java` | Created | Dedicated analytics aggregation service with single-query grouping and dispute threshold calculations. |
| `dto/QuestionAnalyticsDto.java` | Created | DTO encapsulating per-question dispute statistics. |
| `dto/ExamAnalyticsDto.java` | Created | DTO encapsulating exam-level metrics summary. |
| `controller/FacultyController.java` | Modified | Integrated `AnalyticsService` into `/faculty/analytics` endpoint. |
| `test/.../service/QuestionAnalyticsTests.java` | Created | 5 automated tests verifying status breakdown, dispute rate calculation, threshold flagging, empty dataset safety, and authorization. |

---

## 4. Testing & Verification

Executed `QuestionAnalyticsTests` via Maven Surefire:
1. `testAnalyticsAggregationCorrectness`: Verified accurate breakdown of total (2), approved (1), pending (1), and rejected (0) requests across a cohort of 3.
2. `testQuestionDisputeRateAndThresholdFlagging`: Verified 2 requests out of 3 students yields 66.7% dispute rate, correctly triggering flag at 50% threshold, while 0-request question remains normal.
3. `testHighDisputeQuestionsFilter`: Verified `getHighDisputeQuestions` filters only flagged items.
4. `testEmptyDatasetAnalytics`: Verified 0 requests produce 0 counts and 0.0% without division-by-zero errors.
5. `testNonFacultyCannotAccessAnalytics`: Verified non-faculty callers are blocked with `UnauthorizedAccessException`.

**Test Results**: 5 tests run, 0 failures, 0 errors, 0 skipped.

---

## 5. Exit Criteria Verification

- [x] Question-wise re-evaluation frequency is aggregated using real database records.
- [x] High-dispute questions are dynamically identified using configurable thresholds.
- [x] Single-query SQL aggregation prevents $N+1$ query overhead.
- [x] All 5 automated analytics tests passed with 100% success rate.
