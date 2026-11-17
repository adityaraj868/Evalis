# Initial Codebase Audit
## Exam Question Re-evaluation & Review Management System

**Date of Audit**: November 18, 2026  
**Auditor**: Senior Software Architect & Lead Backend Engineer  
**Repository Working Directory**: `/home/epsilon/clg/Enterprise`  

---

## 1. Executive Summary

This audit establishes the baseline architectural, technical, and implementation status of the **Exam Question Re-evaluation & Review Management System** prior to undertaking Phases 2 through 9.

The repository contains an operational Spring Boot 3.4.3 monolithic application with a solid domain model (Phase 1) and fundamental repository layer. The initial build succeeds, and existing unit/integration tests (12 tests) pass with zero failures. However, significant architectural gaps exist in resource authorization, domain exception handling, Data Transfer Object (DTO) usage, lifecycle validation, faculty marks management workflows, and administrative audit filtration.

---

## 2. Technology Stack & Versions

| Component / Layer | Technology | Version | Purpose & Notes |
|---|---|---|---|
| **Language Runtime** | Java (OpenJDK) | 21 (LTS) | Modern Java features (records, switch patterns, text blocks) |
| **Framework** | Spring Boot | 3.4.3 | Application container, autoconfiguration, dependency injection |
| **Security** | Spring Security | 6.4.3 | Authentication, password hashing (BCrypt), HTTP authorization |
| **Persistence / ORM** | Spring Data JPA / Hibernate | 6.6.8.Final | Relational mapping, repositories, transaction management |
| **Relational Database** | MySQL (Production) | 8.0+ | ACID storage, referential integrity, unique constraints |
| **In-Memory Database** | H2 Database (Test/Dev) | 2.3.232 | Fast in-memory testing and development prototyping |
| **Presentation / Views** | Thymeleaf + Extras | 3.1.3 | Server-side template rendering with Security 6 dialect |
| **Frontend Styling** | Bootstrap + Icons | 5.3.3 | Responsive CSS grid, dark/light theme accents, UI components |
| **Validation** | Jakarta Bean Validation | 3.0 (Hibernate Validator 8.0.2) | Server-side constraints (`@NotNull`, `@Size`, `@Min`, `@Max`) |
| **Build & Tooling** | Apache Maven | 3.9+ (Compiler 3.13.0) | Dependency management, build lifecycle, test execution |
| **Testing Framework** | JUnit 5 + Mockito + AssertJ | 5.11.4 / 5.14.2 / 3.26.3 | Comprehensive unit, repository, and MVC mock tests |

---

## 3. Package Structure Analysis

The application follows a standard modular monolithic package structure under `com.example.examreview`:

```
src/main/java/com/example/examreview/
├── ExamReviewApplication.java          # Spring Boot main bootstrap class
├── config/
│   ├── DataInitializer.java            # Seed data runner for non-test profiles
│   └── SecurityConfig.java             # Spring Security filter chain configuration
├── controller/
│   ├── AdminController.java            # Administrative dashboard and audit log routes
│   ├── FacultyController.java          # Faculty exam, review, and analytics endpoints
│   ├── HomeController.java             # Public landing page, login, and error routes
│   └── StudentController.java          # Student exam viewing, request filing and tracking
├── dto/                                # [CURRENTLY EMPTY] Missing structured form DTOs
├── entity/
│   ├── AuditLog.java                   # Audit trail entity
│   ├── Exam.java                       # Examination header and lifecycle entity
│   ├── ExamStatus.java                 # Enum: DRAFT, PUBLISHED, RE_EVALUATION_OPEN, etc.
│   ├── Question.java                   # Question definition with max marks
│   ├── QuestionMark.java               # Student mark per question
│   ├── RecheckRequest.java             # Re-evaluation request entity with unique constraint
│   ├── RequestStatus.java              # Enum: SUBMITTED, UNDER_REVIEW, APPROVED, REJECTED
│   ├── Review.java                     # Faculty decision and review remarks entity
│   ├── ReviewDecision.java             # Enum: APPROVED, REJECTED
│   ├── Role.java                       # Enum: STUDENT, FACULTY, ADMIN
│   ├── StudentResult.java              # Student total marks per exam
│   └── User.java                       # Application user entity
├── exception/                          # [CURRENTLY EMPTY] Missing custom domain exceptions & @ControllerAdvice
├── repository/
│   ├── AuditLogRepository.java         # JPA queries for audit logs
│   ├── ExamRepository.java             # JPA queries for examinations
│   ├── QuestionMarkRepository.java     # JPA queries for question-level marks
│   ├── QuestionRepository.java         # JPA queries for exam questions
│   ├── RecheckRequestRepository.java   # JPA queries with @EntityGraph and custom aggregations
│   ├── ReviewRepository.java           # JPA queries for review records
│   ├── StudentResultRepository.java    # JPA queries for student total results
│   └── UserRepository.java             # JPA queries for users by email and role
├── security/
│   ├── CustomUserDetailsService.java   # UserDetailsService bridging User entity to Spring Security
│   └── RoleBasedAuthenticationSuccessHandler.java # Post-login role-based redirection
├── service/
│   ├── AuditService.java               # Audit logging operations
│   ├── ExamService.java               # Exam creation and status transitions
│   ├── MarksService.java              # Mark recording and recalculation
│   ├── RecheckRequestService.java     # Request submission, window checks, duplicate checks
│   ├── ReviewService.java             # Faculty review processing and score revision
│   └── UserService.java               # User lookup and session context resolution
└── util/                               # [CURRENTLY EMPTY] Utility classes placeholder
```

---

## 4. Current Database Design & Integrity

The relational schema implements 8 tables with appropriate foreign keys, cascading rules, and composite indexes:

1. **`users`**: Primary key `id`. Columns: `email` (UNIQUE), `name`, `password_hash`, `role` (VARCHAR), `active` (BOOLEAN), `created_at`.
2. **`exams`**: Primary key `id`. Columns: `name`, `subject`, `start_date`, `end_date`, `status`, `reevaluation_start`, `reevaluation_end`, timestamps. Indexed on `status`, `start_date`, `end_date`.
3. **`questions`**: Primary key `id`. Foreign key `exam_id` → `exams(id)`. Columns: `question_number`, `question_text`, `max_marks`.
4. **`student_results`**: Primary key `id`. Foreign keys: `student_id` → `users(id)`, `exam_id` → `exams(id)`. Unique constraint: `UNIQUE(student_id, exam_id)`. Column: `total_marks`.
5. **`question_marks`**: Primary key `id`. Foreign keys: `student_id` → `users(id)`, `question_id` → `questions(id)`. Unique constraint: `UNIQUE(student_id, question_id)`. Column: `marks_obtained`.
6. **`recheck_requests`**: Primary key `id`. Foreign keys: `student_id` → `users(id)`, `exam_id` → `exams(id)`, `question_id` → `questions(id)`. Unique constraint: `UNIQUE(student_id, exam_id, question_id)` (ADR-003). Columns: `reason` (TEXT), `status` (VARCHAR), timestamps.
7. **`reviews`**: Primary key `id`. Foreign keys: `request_id` → `recheck_requests(id)`, `faculty_id` → `users(id)`. Columns: `decision` (VARCHAR), `comments` (TEXT), `revised_marks` (DOUBLE), `reviewed_at`.
8. **`audit_logs`**: Primary key `id`. Foreign key `user_id` → `users(id)`. Columns: `action` (VARCHAR), `description` (TEXT), `timestamp`.

---

## 5. Security & Authentication Audit

### Implemented Controls
- Spring Security `SecurityFilterChain` restricts endpoints:
  - `/student/**` → `hasRole('STUDENT')`
  - `/faculty/**` → `hasRole('FACULTY')`
  - `/admin/**` → `hasRole('ADMIN')`
  - `/login`, `/`, static assets, `/403` → `permitAll()`
- Passwords stored as BCrypt hashes (`BCryptPasswordEncoder`).
- Role-based redirect on successful authentication via `RoleBasedAuthenticationSuccessHandler`.

### Security Vulnerabilities & Gaps
1. **Horizontal Privilege Escalation (IDOR)**:
   - In `StudentController.examDetail(/student/exams/{id})`, any authenticated student can access any exam's breakdown if they know the exam ID, though an error is shown if no `StudentResult` exists.
   - In `StudentController.requestDetail(/student/requests/{id})`, an ownership check `!request.getStudent().getId().equals(student.getId())` is performed manually in the controller. However, backend services lack fine-grained security assertions.
2. **Missing Method-Level Security**: `@EnableMethodSecurity` is not enabled, leaving service layer methods unprotected if called from alternate interfaces or scheduled jobs.
3. **Missing Custom 403 / 401 Exception Translation**: While `/403` template exists, Spring Security exceptions thrown during authorization checks in controllers/services can leak default white-label error views if unhandled.

---

## 6. Test Suite Status

Currently, 12 tests are configured and passing:
- `ExamReviewApplicationTests`: Context load verification (1 test).
- `HomeControllerSmokeTest`: Public and authenticated dashboard route rendering (3 tests).
- `DomainRepositoryTests`: JPA entity persistence, composite unique constraints (`UNIQUE(student_id, exam_id, question_id)`, `UNIQUE(student_id, question_id)`, `UNIQUE(student_id, exam_id)`), custom aggregation queries, and audit logging (8 tests).

**Execution Time**: ~11.7 seconds on H2 in-memory profile.  
**Failures**: 0. **Errors**: 0. **Skipped**: 0.

---

## 7. Architectural Weaknesses & Gaps by Implementation Phase

### Phase 2: Authentication & Authorization
- Controllers extract `User` using `userService.getCurrentUser()` which returns `null` if unauthenticated. Controller methods should be defensive.
- Access denied handling should clearly distinguish between unauthenticated (401 -> redirect to login with callback) and unauthorized (403 -> forbidden view with user-friendly message).
- Comprehensive security tests covering student, faculty, admin, and unauthorized cross-role access do not exist.

### Phase 3: Examination & Question Management
- Examination lifecycle state machine is incomplete:
  - Transition rules (`DRAFT` → `PUBLISHED` → `RE_EVALUATION_OPEN` → `CLOSED`) are not strictly validated in `ExamService`.
  - Publishing an exam with zero questions or total marks of 0 is currently allowed.
  - Modifying an exam after it has opened for re-evaluation is not blocked.
- Question management is limited to initial creation in `FacultyController.createExam`. Adding or editing individual questions is not supported.

### Phase 4: Marks Management
- Marks entry is only handled during database seeding (`DataInitializer`) or single record helper in `MarksService`.
- There is no faculty web interface or batch API for entering student question marks.
- Total calculation in `MarksService.recalculateStudentResult` does not validate whether total marks matches the sum of maximum possible marks.
- Marks bounds validation (`0.0 <= marksObtained <= maxMarks`) is not consistently enforced in `MarksService.recordMark`.

### Phase 5: Re-evaluation Request Core
- Core submission logic in `RecheckRequestService` is sound with `UNIQUE` constraint and window check.
- However, form validation errors are handled via raw `IllegalArgumentException` and caught with flash attributes. Needs structured DTO validation (`@Valid`) and domain exceptions.

### Phase 6: Request Tracking
- The student request view does not show a detailed status progression timeline (e.g., Submitted at X, Reviewed by Faculty at Y, Final Marks updated at Z).
- Request status updates from `SUBMITTED` to `UNDER_REVIEW` should automatically trigger when faculty opens the request.

### Phase 7: Faculty Review Workflow
- Review decision logic is implemented in `ReviewService`, but state transition guards (e.g. preventing reviewing an already APPROVED/REJECTED request) are missing.
- When revised marks are awarded, there is no explicit check that the reviewer is authorized for that specific examination/department.

### Phase 8: Analytics
- Analytics currently runs on-demand with raw query counts. Needs a dedicated, testable `AnalyticsService` calculating:
  - Total requests per examination.
  - Pending, approved, and rejected request counts and percentages.
  - High-dispute question identification based on a configurable percentage threshold.
  - Cohort statistics (average disputed question score vs overall question score).

### Phase 9: Audit Trail
- `AuditLog` entity only stores a simple user reference, action string, and description text.
- Missing:
  - Affected resource type (`EXAM`, `QUESTION`, `MARKS`, `REQUEST`, `REVIEW`).
  - Affected resource ID.
  - Previous value / updated value structured fields.
  - Administrative search and filtering (by actor, action type, resource, date range).
  - Immutability guards preventing update/deletion of audit records.

---

## 8. Action Plan for Phases 2–9

1. **Phase 2**: Harden Spring Security, add Method Security (`@EnableMethodSecurity`), implement custom domain exceptions (`ResourceNotFoundException`, `AccessDeniedException`, `ValidationException`), configure centralized `@ControllerAdvice`, and build comprehensive security tests.
2. **Phase 3**: Refactor `ExamService` with strict state machine validation (`DRAFT` → `PUBLISHED` → `RE_EVALUATION_OPEN` → `CLOSED`), implement examination editing and question management, and add validation tests.
3. **Phase 4**: Implement complete marks management service with batch entry, upper/lower bound checks (`0 <= mark <= maxMarks`), transactional recalculation, and faculty marks recording UI.
4. **Phase 5**: Refine re-evaluation request submission with structured DTOs, validation annotations, concurrent race condition tests, and clear error translation.
5. **Phase 6**: Build enhanced student request tracking with detailed status timeline, transition auditing, and strict student data isolation tests.
6. **Phase 7**: Implement strict faculty review workflow state transitions (`UNDER_REVIEW` upon opening, atomic `APPROVED`/`REJECTED` with marks revision and transactional consistency), bounds validation, and rollback tests.
7. **Phase 8**: Implement dedicated `AnalyticsService` with robust aggregation, dispute frequency threshold detection, and tests for empty datasets and varied cohort distributions.
8. **Phase 9**: Upgrade `AuditLog` to structured audit records (resource type, resource ID, actor, action, previous/updated values), integrate audit events into all services, add admin filtering and tamper-proof protection, and write audit integrity tests.
