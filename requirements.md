# Requirements Specification
## Exam Question Re-evaluation & Review Management System

## 1. Product Definition

The system is a secure web application that digitizes the examination re-evaluation process.

After examination results are released, students can view question-wise marks and submit a re-evaluation request for a specific question with a reason. The system validates and stores requests, aggregates them question-wise, and gives faculty a dashboard for analysis and review.

Faculty retains final authority over the review decision.

Core principle:

`Students raise requests → System aggregates requests → Faculty reviews → Faculty makes the final decision`

---

## 2. Actors

### STUDENT

The student can:
- Register/login.
- View available examinations.
- View examination results.
- View question-wise marks.
- Submit a question-specific re-evaluation request.
- Provide a reason.
- Track request status.
- View final decisions.
- View revised marks where applicable.

### FACULTY

Faculty can:
- Login.
- Create/manage examinations where authorized.
- Add/manage questions.
- Manage student marks where authorized.
- Open/close re-evaluation periods.
- View requests.
- Analyze question-wise request counts.
- Review requests.
- Approve or reject requests.
- Record review comments.
- Record revised marks.
- View relevant audit logs.

### ADMIN

Admin can perform administrative functions defined by the implementation, including user/exam management and audit access.

Do not invent powers beyond the documented requirements without explicit approval.

---

## 3. Examination Lifecycle

An examination must have enough state information to determine whether marks and re-evaluation actions are available.

Recommended states:

`DRAFT → PUBLISHED → RE_EVALUATION_OPEN → RE_EVALUATION_CLOSED → ARCHIVED`

The exact transition names may be refined during implementation, but illegal transitions must be rejected.

---

## 4. Functional Requirements

### FR-01 Authentication

Users shall be able to securely authenticate.

### FR-02 Authorization

The application shall restrict functionality according to role.

Required roles:
- STUDENT
- FACULTY
- ADMIN

### FR-03 Student Management

Authorized staff shall be able to create/update/remove/view students as required by the proposal.

### FR-04 Examination Management

Authorized users shall be able to:
- Create examinations.
- Define examination name.
- Define subject.
- Define examination dates.
- Manage examination status.
- Publish examination information.
- Open and close the re-evaluation period.

### FR-05 Question Management

Authorized faculty/admin users shall be able to:
- Add questions to an examination.
- Edit questions where allowed.
- Delete questions before dependent records make deletion unsafe.
- Define question text.
- Define maximum marks.

### FR-06 Marks Management

The system shall store and display:
- Student result for an examination.
- Question-wise marks.
- Maximum marks per question.

Marks must belong to the correct student, examination, and question.

### FR-07 Student Examination View

A student shall be able to view examinations/results for which they have valid records.

Example:

```text
Q1  8/10
Q2  3/10
Q3  9/10
Q4  2/10
Q5 10/10
```

### FR-08 Re-evaluation Request

A student shall be able to select a specific question and submit:
- Examination
- Question
- Reason

The authenticated student identity must come from the server-side security context.

### FR-09 Request Validation

Before storing a request, the server must verify:
1. Student is authenticated.
2. Student is actually associated with the examination.
3. The examination permits re-evaluation.
4. The question belongs to that examination.
5. The student has a valid mark for that question.
6. The student has not already submitted a request for that question.
7. The reason satisfies input validation rules.

### FR-10 Duplicate Prevention

A student must not be able to submit multiple requests for the same student/exam/question combination.

Application-level validation must be supplemented by a database unique constraint:

`UNIQUE(student_id, exam_id, question_id)`

Concurrent duplicate submissions must be handled safely.

### FR-11 Request Status

Requests shall support the lifecycle:

`SUBMITTED → UNDER_REVIEW → APPROVED / REJECTED → COMPLETED`

The implementation must prevent nonsensical state transitions.

### FR-12 Request Tracking

Students shall be able to see:
- Question
- Reason
- Submission time
- Current status
- Faculty decision when available
- Revised marks when available

### FR-13 Request Aggregation

The system shall calculate question-wise request counts.

Example:

```text
Q1 → 5 requests
Q2 → 12 requests
Q3 → 4 requests
Q4 → 67 requests
Q5 → 3 requests
```

### FR-14 Question Flagging

Automatic threshold-based flagging is an optional advanced feature.

Example:
- 100 eligible students
- 42 requests for Q4
- threshold 30%
- Q4 is flagged

The threshold must be configurable rather than hardcoded if this feature is implemented.

### FR-15 Faculty Review

Faculty shall be able to inspect:
- Question
- Request count
- Student reasons
- Request status
- Review history

Faculty can make the final decision.

### FR-16 Review Decision

Faculty can:
- Approve
- Reject

Faculty may also add comments.

### FR-17 Revised Marks

Where a review changes marks, faculty can record revised marks.

Validation:
- Revised marks must not be negative.
- Revised marks must not exceed the question maximum marks.
- Revised marks must belong to the correct student/question/exam.
- A mark change must be auditable.

### FR-18 Audit Logging

Important actions shall create audit records.

At minimum consider:
- Login/security events where appropriate
- Examination creation/update
- Question changes
- Marks changes
- Re-evaluation request submission
- Review decision
- Revised marks
- Opening/closing re-evaluation

Audit records should include:
- User
- Action
- Timestamp
- Description

Do not store passwords or authentication secrets in audit logs.

### FR-19 Dashboards

#### Student Dashboard

Should show:
- Available examinations
- Results
- Question-wise marks
- Re-evaluation availability
- Submitted requests
- Request statuses
- Final decisions

#### Faculty Dashboard

Should show:
- Total examinations
- Total requests
- Question-wise request counts
- Flagged questions where enabled
- Pending reviews
- Approved/rejected requests
- Revised marks

### FR-20 Notification Module

Email/in-app notifications are optional.

Do not make the baseline project dependent on an external notification provider.

---

## 5. Non-Functional Requirements

### NFR-01 Security

Protect credentials and restrict unauthorized access.

### NFR-02 Reliability

Exam, marks, request, review, and audit data must be stored and retrieved accurately.

### NFR-03 Performance

The application should remain responsive for normal college-scale usage.

### NFR-04 Usability

Students and faculty should be able to understand the workflow without training.

### NFR-05 Scalability

The relational design should support additional examinations and students without redesigning the core model.

### NFR-06 Maintainability

Use modular, layered code with clear separation of concerns.

### NFR-07 Data Integrity

Use foreign keys, validation, transactions, and database constraints to preserve relationships and prevent duplicate requests.

---

## 6. Core Acceptance Criteria

The baseline project is complete when:

- Student can log in.
- Faculty/admin can log in.
- Role restrictions work.
- Authorized users can create an examination.
- Questions can be associated with an examination.
- Question maximum marks can be stored.
- Student question-wise marks can be displayed.
- Re-evaluation can be opened and closed.
- Eligible student can submit a request with a reason.
- Invalid requests are rejected.
- Duplicate request is rejected.
- Database prevents duplicate requests under concurrent submission.
- Faculty can see question-wise request counts.
- Faculty can inspect requests.
- Faculty can approve/reject requests.
- Revised marks can be recorded safely.
- Student can track status.
- Audit records are created for important actions.
- Automated tests cover critical workflow and security paths.

---

## 7. Explicit Non-Goals

Do not implement in the baseline:
- Online exam conduction
- Automatic answer evaluation
- OCR of handwritten papers
- University-wide deployment
- Government-scale examination infrastructure
- Blockchain
- Biometrics
- Facial recognition
- Microservices
- Kubernetes
- Custom cryptography
- AI judging whether a student's answer deserves more marks

The proposal explicitly states that the system does not automatically determine whether an answer is correct; faculty retains final authority.
