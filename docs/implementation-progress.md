# Implementation Progress

Tracking against [implementation-plan.md](file:///home/epsilon/clg/Enterprise/implementation-plan.md) following the rule:
`Inspect → Plan → Implement → Test → Review → Document`

---

## Phase 0 — Project Bootstrap: COMPLETED
- Spring Boot 3.4.3 Maven project configured with Java 21
- Dependencies added: Spring Web, Thymeleaf, Spring Security, Spring Data JPA, MySQL driver, H2 (test/dev), Validation, Testing dependencies
- Established package structure & base theme/layout
- Exit condition verified: Application starts, basic page renders, tests execute.

---

## Phase 1 — Domain Model: COMPLETED
- Implemented Enums:
  - `Role` (`STUDENT`, `FACULTY`, `ADMIN`)
  - `ExamStatus` (`DRAFT`, `PUBLISHED`, `RE_EVALUATION_OPEN`, `RE_EVALUATION_CLOSED`, `ARCHIVED`)
  - `RequestStatus` (`SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`, `COMPLETED`)
  - `ReviewDecision` (`APPROVED`, `REJECTED`)
- Implemented Entities:
  - `User` (`users` table, email uniqueness, role indexing)
  - `Exam` (`exams` table, status and lifecycle dates, ordered question mapping)
  - `Question` (`questions` table, exam relationship, max marks)
  - `StudentResult` (`student_results` table, `UNIQUE(student_id, exam_id)`)
  - `QuestionMark` (`question_marks` table, `UNIQUE(student_id, question_id)`)
  - `RecheckRequest` (`recheck_requests` table, enforced ADR-003 `UNIQUE(student_id, exam_id, question_id)`)
  - `Review` (`reviews` table, faculty association, revised marks, decisions)
  - `AuditLog` (`audit_logs` table, user and action auditing)
- Implemented Repositories:
  - `UserRepository`
  - `ExamRepository`
  - `QuestionRepository`
  - `StudentResultRepository`
  - `QuestionMarkRepository`
  - `RecheckRequestRepository` (with custom question aggregation count query)
  - `ReviewRepository`
  - `AuditLogRepository`
- Tests Added & Verified (`DomainRepositoryTests`):
  - User repository lookups by email & role
  - Exam and Question persistence and ordering
  - `StudentResult` uniqueness enforcement
  - `QuestionMark` uniqueness enforcement
  - `RecheckRequest` unique constraint violation handling (ADR-003)
  - Question request aggregation query verification
  - Faculty review persistence and history linkage
  - AuditLog recording and chronological ordering
- Exit condition verified: Schema starts cleanly with Hibernate 6, all 10 tests pass without errors or warnings.
