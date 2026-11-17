# Re-evaluation Workflow & Request Lifecycle
## Exam Question Re-evaluation & Review Management System

### 1. Re-evaluation Lifecycle Overview
The core value proposition of the system is granular, question-level re-evaluation. A request progresses through four discrete states:
`SUBMITTED → UNDER_REVIEW → APPROVED / REJECTED`.

```mermaid
stateDiagram-v2
    [*] --> SUBMITTED : Student Submits Request
    SUBMITTED --> UNDER_REVIEW : Faculty Opens Request Details
    UNDER_REVIEW --> APPROVED : Faculty Approves & Enters Revised Marks
    UNDER_REVIEW --> REJECTED : Faculty Rejects with Feedback
    APPROVED --> [*]
    REJECTED --> [*]

    note right of APPROVED
        Question mark updated.
        Total marks recalculated atomically.
        Decision becomes immutable.
    end note

    note right of REJECTED
        Marks remain untouched.
        Decision becomes immutable.
    end note
```

---

### 2. Detailed Request Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student
    actor Faculty as Faculty
    participant StudentCtrl as StudentController
    participant FacultyCtrl as FacultyController
    participant ReqService as RecheckRequestService
    participant RevService as ReviewService
    participant MarksService as MarksService
    participant AuditService as AuditService
    participant DB as Relational Database

    Note over Student,DB: 1. Submission Phase
    Student->>StudentCtrl: POST /student/requests (examId, questionId, reason)
    StudentCtrl->>ReqService: submitRequest(studentId, examId, questionId, reason)
    ReqService->>DB: Validate Window, Enrolled, Mark Exists, No Duplicate
    ReqService->>DB: INSERT into RECHECK_REQUESTS (status='SUBMITTED')
    ReqService->>AuditService: logEvent("REQUEST_SUBMITTED")
    AuditService->>DB: INSERT into AUDIT_LOGS
    ReqService-->>StudentCtrl: Saved RecheckRequest
    StudentCtrl-->>Student: Redirect to Dashboard (Success alert)

    Note over Faculty,DB: 2. Inspection & Review Phase
    Faculty->>FacultyCtrl: GET /faculty/requests/{id}
    FacultyCtrl->>ReqService: markUnderReview(id, facultyUser)
    ReqService->>DB: UPDATE RECHECK_REQUESTS status='UNDER_REVIEW'
    ReqService->>AuditService: logEvent("REQUEST_UNDER_REVIEW")
    FacultyCtrl-->>Faculty: Render Review Evaluation Screen

    Note over Faculty,DB: 3. Decision Phase
    Faculty->>FacultyCtrl: POST /faculty/requests/{id}/review (decision, revisedMarks, comments)
    FacultyCtrl->>RevService: completeReview(id, facultyUser, decision, revisedMarks, comments)
    alt Decision == APPROVED
        RevService->>MarksService: updateQuestionMark(studentId, questionId, revisedMarks)
        MarksService->>DB: UPDATE QUESTION_MARKS set marks_obtained = revisedMarks
        MarksService->>MarksService: recalculateTotal(studentResult)
        MarksService->>DB: UPDATE STUDENT_RESULTS set total_marks = sum(marks)
    end
    RevService->>DB: INSERT into REVIEWS (...)
    RevService->>DB: UPDATE RECHECK_REQUESTS status = decision
    RevService->>AuditService: logEvent("REVIEW_COMPLETED", previousMarks, revisedMarks)
    AuditService->>DB: INSERT into AUDIT_LOGS
    RevService-->>FacultyCtrl: Success
    FacultyCtrl-->>Faculty: Redirect to Requests Dashboard
```

---

### 3. Business Constraints & Immutability Rules
1. **Window Guard**: Submissions are permitted only while `exam.reevaluationStart <= now <= exam.reevaluationEnd` and `exam.status == RE_EVALUATION_OPEN`.
2. **Duplicate Guard**: Enforced at both application level and database level (`UNIQUE(student_id, exam_id, question_id)`).
3. **Immutability of Decisions**: Once a request reaches `APPROVED` or `REJECTED`, any subsequent review invocation throws `InvalidStateTransitionException`.
4. **Marks Bounds**: If approved, revised marks must satisfy $0.0 \le \text{revisedMarks} \le \text{question.maxMarks}$.
