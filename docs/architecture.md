# Architecture

## Architecture Style

Use a **modular monolith with layered architecture**.

```text
Browser
   │
   ▼
Thymeleaf Views
   │
   ▼
Controllers
   │
   ▼
Services / Business Rules
   │
   ▼
Repositories
   │
   ▼
MySQL
```

## Suggested Package Structure

```text
com.example.examreview/
├── config/
├── controller/
├── dto/
├── entity/
├── exception/
├── repository/
├── security/
├── service/
└── util/
```

Templates:

```text
src/main/resources/templates/
├── auth/
├── student/
├── faculty/
├── admin/
├── exams/
├── requests/
├── fragments/
└── error/
```

Static resources:

```text
src/main/resources/static/
├── css/
├── js/
└── images/
```

## Layer Responsibilities

### Controller

Responsible for:
- HTTP routing
- Request DTO binding
- Basic validation
- Selecting views
- Delegating to services

Do not place core workflow rules in controllers.

### Service

Responsible for:
- Examination rules
- Re-evaluation eligibility
- Duplicate prevention
- Request state transitions
- Review workflow
- Mark revision rules
- Transactions

### Repository

Responsible for:
- Database persistence/querying
- Aggregation queries
- Existence checks

### Entity

Persistent domain model.

### DTO

Used to avoid exposing mutable/internal entity fields directly to web forms.

### Security

Responsible for:
- Authentication
- Authorization
- Password encoding
- Session security
- Role enforcement

---

## Critical Request Submission Flow

```text
POST request
     ↓
Authenticated principal
     ↓
Load exam
     ↓
Check re-evaluation period
     ↓
Check student belongs to exam
     ↓
Check question belongs to exam
     ↓
Check student's question mark exists
     ↓
Attempt request insert
     ↓
UNIQUE(student_id, exam_id, question_id)
     ↓
Commit transaction
     ↓
Return success
```

Do not rely only on:

`check existing request → insert`

because concurrent requests can both pass the check.

The database constraint is the final duplicate-protection mechanism.

## Transaction Boundaries

At minimum:
- Re-evaluation request submission
- Review decision + revised marks
- Important coupled marks updates

should use appropriate transaction boundaries.

## Review + Revised Marks

If approving a request and changing marks, the operation should be designed so that related state changes cannot leave the system half-updated.

Example:

```text
Review decision
      +
Revised marks
      +
Audit record
```

should be handled atomically where the business rule requires it.

## Aggregation

Question-wise request counts should be derived from persisted request data.

Do not maintain independent counters as the only source of truth.

## Time

Use server-side time for:
- Exam dates
- Re-evaluation opening/closing
- Request submission timestamps
- Review timestamps
- Audit timestamps

Do not trust the browser's clock for eligibility decisions.

## No Redis

Redis is intentionally excluded from the current baseline.

Do not introduce caching infrastructure until the core system is complete and a concrete need is identified.
