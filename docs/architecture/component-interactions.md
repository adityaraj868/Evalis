# Component Interactions
## Exam Question Re-evaluation & Review Management System

### 1. Inter-Service Communication Flow
Within the monolithic architecture, service components interact via strict Java interfaces and Spring Dependency Injection. Direct cross-talk is kept minimal and purposeful to maintain loose coupling.

```
       +---------------------------------------------+
       |             FacultyController               |
       +---------------------------------------------+
               |                       |
               v                       v
     +-------------------+   +--------------------+
     |   ReviewService   |   |  AnalyticsService  |
     +-------------------+   +--------------------+
         |           |                  |
         |           v                  v
         |   +----------------+   +------------------------+
         |   |  MarksService  |   | RecheckRequestRepo     |
         |   +----------------+   +------------------------+
         |           |
         v           v
    +-----------------------+
    |     AuditService      |
    +-----------------------+
                |
                v
    +-----------------------+
    |   AuditLogRepository  |
    +-----------------------+
```

---

### 2. Primary Workflow Collaborations

#### 2.1 Re-evaluation Submission Workflow
When a student submits a re-evaluation request:
1. `StudentController` invokes `UserService.getRequiredCurrentUser()` to establish identity.
2. `StudentController` invokes `RecheckRequestService.submitRequest(...)` with form parameters.
3. `RecheckRequestService` collaborates with:
   - `ExamRepository` to fetch the exam and verify its status is `RE_EVALUATION_OPEN` and current timestamp is within window.
   - `QuestionRepository` to ensure the question belongs to the specified exam.
   - `QuestionMarkRepository` to verify the student actually has a mark recorded for this question.
   - `RecheckRequestRepository` to verify no existing request exists for this `(student, exam, question)`.
4. `RecheckRequestRepository.save(...)` persists the entity in `SUBMITTED` status.
5. `AuditService.logEvent(...)` records a structured audit log (`REQUEST_SUBMITTED`).

#### 2.2 Faculty Review and Mark Adjustment Workflow
When faculty renders a decision on a disputed question:
1. `FacultyController` verifies faculty authentication and passes `ReviewFormDto` to `ReviewService.completeReview(...)`.
2. `ReviewService` validates:
   - Request exists and is in `SUBMITTED` or `UNDER_REVIEW` status (decisions are immutable).
   - Remarks are present.
   - Decision is valid (`APPROVED` or `REJECTED`).
   - If `APPROVED`, revised marks are validated against question `maxMarks`.
3. If `APPROVED`:
   - `ReviewService` calls `MarksService.updateQuestionMark(...)`.
   - `MarksService` updates the `QuestionMark.marksObtained` and calls `recalculateTotal(...)` on `StudentResult`.
   - Both question mark and total result are updated within the same transaction.
4. `ReviewRepository.save(...)` stores the review record.
5. `RecheckRequest` status is transitioned to `APPROVED` or `REJECTED`.
6. `AuditService.logEvent(...)` records a comprehensive audit event (`REVIEW_COMPLETED`) capturing previous marks, revised marks, reviewer ID, and comments.

#### 2.3 Analytics Computation Workflow
When faculty visits `/faculty/analytics`:
1. `FacultyController` calls `AnalyticsService.getExamAnalytics(examId)`.
2. `AnalyticsService` queries `ExamRepository` for question details and `RecheckRequestRepository.countRequestsByQuestionForExam(examId)` for dispute counts in a single aggregation query.
3. Total student enrollment is queried from `StudentResultRepository`.
4. Dispute rates are computed per question, applying dispute alert flags when dispute rate exceeds the threshold.
5. The enriched DTO is returned to `FacultyController` to populate the view.
