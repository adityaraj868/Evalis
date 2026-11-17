# System Overview
## Exam Question Re-evaluation & Review Management System

### 1. Introduction & Problem Statement
In traditional university examination systems, post-examination evaluations and student grievance redressal suffer from several recurring friction points:
- **Opaque Paper-based Processes**: Re-evaluation requests submitted via physical forms are frequently delayed, misplaced, or difficult to trace.
- **Coarse-grained Re-evaluations**: Conventional systems mandate re-checking the entire paper, generating substantial overhead for faculty when students typically dispute only specific questions or marking inconsistencies.
- **Lack of Transparency & Auditability**: When marks are altered, there is rarely a comprehensive, immutable audit log of who made the change, the prior score, the revised score, and the academic justification.
- **Absence of Actionable Pedagogical Insights**: Institutions fail to identify questions with unusually high grievance rates that might point to ambiguous phrasing, incorrect answer keys, or out-of-syllabus content.

The **Exam Question Re-evaluation & Review Management System** solves these challenges by offering a granular, question-level re-evaluation platform built with Spring Boot 3, Java 21, and Thymeleaf. It provides role-specific portals for Students, Faculty, and Administrators, ensuring transparency, security, and academic integrity.

---

### 2. High-Level System Architecture

The platform is designed as a **Layered Modular Monolith**, avoiding unnecessary distributed systems complexity while enforcing strict separation of concerns, transactional consistency, and defense-in-depth security.

```
       +--------------------------------------------------------+
       |                  Web Browser / Client                  |
       +--------------------------------------------------------+
                                   | HTTP / HTTPS
                                   v
+----------------------------------------------------------------------+
|                     Presentation Layer (Web MVC)                     |
|  - StudentController      - FacultyController     - AdminController  |
|  - AuthController         - GlobalExceptionHandler (400, 403, 404)   |
|  - Thymeleaf Server-Side Rendering (Bootstrap 5 & Custom CSS)        |
+----------------------------------------------------------------------+
                                   | DTOs & Domain Models
                                   v
+----------------------------------------------------------------------+
|                      Security & Interceptor Layer                    |
|  - Spring Security Filter Chain   - RoleBasedSuccessHandler          |
|  - BCryptPasswordEncoder          - Method Security (@PreAuthorize)  |
+----------------------------------------------------------------------+
                                   | Authorized Calls
                                   v
+----------------------------------------------------------------------+
|                      Business Logic Layer (Services)                 |
|  - ExamService             - MarksService         - ReviewService    |
|  - RecheckRequestService   - AnalyticsService     - AuditService     |
|  - UserService                                                       |
|  - Declarative Transaction Management (@Transactional)               |
+----------------------------------------------------------------------+
                                   | Entities & JPA Criteria
                                   v
+----------------------------------------------------------------------+
|                     Data Access Layer (Spring Data JPA)              |
|  - UserRepository          - ExamRepository       - QuestionRepo     |
|  - QuestionMarkRepository  - StudentResultRepo    - RecheckRepo      |
|  - ReviewRepository        - AuditLogRepository                      |
+----------------------------------------------------------------------+
                                   | SQL / JDBC / Connection Pool
                                   v
+----------------------------------------------------------------------+
|                         Relational Database                          |
|  - H2 In-Memory (Test/Dev) / MySQL 8.0 (Production)                  |
|  - ACID Transactions, Composite Unique Constraints, Foreign Keys     |
+----------------------------------------------------------------------+
```

---

### 3. Core Modules and Capabilities

1. **Identity & Access Management (IAM)**:
   - Three distinct roles: `STUDENT`, `FACULTY`, `ADMIN`.
   - Form-based session authentication with BCrypt password hashing.
   - Intelligent role-based redirection post-login.
   - Resource-level authorization preventing Horizontal Privilege Escalation (IDOR).

2. **Examination & Question Lifecycle Management**:
   - Examination lifecycle states: `DRAFT → PUBLISHED → RE_EVALUATION_OPEN → RE_EVALUATION_CLOSED → ARCHIVED`.
   - Strict immutability rules prevent modifying exams or adding questions once published.
   - Configurable time-bounded re-evaluation windows (`reevaluationStart` to `reevaluationEnd`).

3. **Granular Question-Level Marks Management**:
   - Question marks stored individually per student.
   - Upper and lower bounds validation ($0.0 \le \text{mark} \le \text{maxMarks}$).
   - Automatic atomic total score recalculation and synchronization in `StudentResult`.

4. **Re-evaluation Request Core & Tracking**:
   - Students submit requests targeting specific questions with mandatory minimum rationale ($\ge 5$ characters).
   - Composite uniqueness constraint: `UNIQUE(student_id, exam_id, question_id)` guarantees at most one active request per student per question.
   - Lifecycle tracking: `SUBMITTED → UNDER_REVIEW → APPROVED / REJECTED`.
   - Automated progression: Opening a submitted request marks it `UNDER_REVIEW`.

5. **Faculty Review & Score Harmonization**:
   - Faculty evaluates disputes against the original question and student marks.
   - On approval, revised marks update `QuestionMark` and recalculate `StudentResult` atomically within a database transaction.
   - On rejection, original marks are locked and untouched.
   - Review decisions are immutable once rendered.

6. **Question Dispute Analytics**:
   - Question dispute frequency aggregation via single SQL group-by queries.
   - Anomaly detection flag for questions exceeding configurable dispute thresholds (default: 15%).
   - Dispute rate computation with zero-division safety.

7. **Centralized Immutable Audit Trail**:
   - Captures actor ID, action type, resource type, resource ID, previous values, updated values, human descriptions, and timestamps.
   - Filterable admin interface supporting multi-criteria search.
