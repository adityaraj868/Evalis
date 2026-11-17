# Sequence Diagrams
## Exam Question Re-evaluation & Review Management System

### 1. Request Submission Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student (Browser)
    participant Ctrl as StudentController
    participant Svc as RecheckRequestService
    participant Repo as RecheckRequestRepository
    participant Audit as AuditService
    participant DB as Relational Database

    Student->>Ctrl: POST /student/requests (examId, questionId, reason)
    Ctrl->>Svc: submitRequest(studentId, examId, questionId, reason)
    Svc->>DB: Check exam status == RE_EVALUATION_OPEN & now in window
    Svc->>DB: Check question belongs to exam & marks exist
    Svc->>Repo: existsByStudentAndExamAndQuestion(student, exam, question)
    alt Request Already Exists
        Repo-->>Svc: true
        Svc-->>Ctrl: throw DuplicateRequestException
        Ctrl-->>Student: Render Error View / Message (HTTP 400)
    else No Prior Request
        Repo-->>Svc: false
        Svc->>Repo: save(new RecheckRequest(SUBMITTED))
        Repo->>DB: INSERT into RECHECK_REQUESTS
        Svc->>Audit: logEvent("REQUEST_SUBMITTED", request)
        Audit->>DB: INSERT into AUDIT_LOGS
        Svc-->>Ctrl: Saved Entity
        Ctrl-->>Student: HTTP 302 Redirect to /student/dashboard
    end
```

---

### 2. Faculty Review Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Faculty as Faculty (Browser)
    participant Ctrl as FacultyController
    participant RevSvc as ReviewService
    participant MarksSvc as MarksService
    participant Audit as AuditService
    participant DB as Relational Database

    Faculty->>Ctrl: POST /faculty/requests/{id}/review (decision, revisedMarks, comments)
    Ctrl->>RevSvc: completeReview(id, facultyUser, decision, revisedMarks, comments)
    RevSvc->>DB: Fetch RecheckRequest & assert status in [SUBMITTED, UNDER_REVIEW]
    alt Decision == APPROVED
        RevSvc->>MarksSvc: updateQuestionMark(studentId, questionId, revisedMarks)
        MarksSvc->>DB: UPDATE question_marks SET marks_obtained = revisedMarks
        MarksSvc->>MarksSvc: recalculateTotal(studentResult)
        MarksSvc->>DB: UPDATE student_results SET total_marks = sum(marks)
    end
    RevSvc->>DB: INSERT into reviews (decision, comments, revised_marks)
    RevSvc->>DB: UPDATE recheck_requests SET status = decision
    RevSvc->>Audit: logEvent("REVIEW_COMPLETED", previousMarks, revisedMarks)
    Audit->>DB: INSERT into audit_logs
    RevSvc-->>Ctrl: Success
    Ctrl-->>Faculty: HTTP 302 Redirect to /faculty/requests
```

---

### 3. Exported Diagram Files
- Sequence Diagram (Submission): [sequence-diagram-submission.svg](sequence-diagram-submission.svg) | [PNG](sequence-diagram-submission.png)
- Sequence Diagram (Review): [sequence-diagram-review.svg](sequence-diagram-review.svg) | [PNG](sequence-diagram-review.png)
