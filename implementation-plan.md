# Implementation Plan

Build the application incrementally.

## Phase 0 — Project Bootstrap

- Create Spring Boot Maven project.
- Configure Java 21.
- Add Spring Web.
- Add Thymeleaf.
- Add Spring Security.
- Add Spring Data JPA.
- Add MySQL driver.
- Add validation.
- Add testing dependencies.
- Establish package structure.
- Establish common layout/theme.

Exit condition:
- Application starts.
- Basic page renders.
- Tests execute.

## Phase 1 — Domain Model

Implement:
- User
- Exam
- Question
- StudentResult
- QuestionMark
- RecheckRequest
- Review
- AuditLog

Create relationships and database constraints.

Exit condition:
- Schema starts cleanly.
- Repository tests pass.

## Phase 2 — Authentication & Authorization

Implement:
- Login
- Logout
- Password hashing
- STUDENT/FACULTY/ADMIN roles
- Route protection
- Access-denied page

Exit condition:
- Each role reaches only permitted areas.

## Phase 3 — Examination & Question Management

Implement:
- Exam creation
- Exam editing
- Exam status
- Questions
- Maximum marks
- Exam publishing

Exit condition:
- Faculty/admin can configure an exam.

## Phase 4 — Marks Management

Implement:
- Student result
- Question-wise marks
- Student result view
- Faculty marks management

Exit condition:
- Student sees correct question-wise marks.

## Phase 5 — Re-evaluation Request Core

Implement:
- Re-evaluation period
- Student eligibility
- Request form
- Reason validation
- Request creation
- Duplicate prevention
- Transaction handling

Exit condition:
- Valid request succeeds.
- Invalid/duplicate request fails.
- Database uniqueness is enforced.

## Phase 6 — Request Tracking

Implement:
- Student request list
- Request details
- Status lifecycle
- Student-visible decision state

Exit condition:
- Student can track the complete lifecycle.

## Phase 7 — Faculty Review

Implement:
- Request list
- Question-wise grouping
- Request detail
- Review decision
- Comments
- Revised marks

Exit condition:
- Faculty can process a request safely.

## Phase 8 — Analytics

Implement:
- Request counts by question
- Request percentages
- Optional threshold/flagging
- Faculty dashboard

Exit condition:
- Aggregates match database records.

## Phase 9 — Audit Logs

Implement:
- Audit entity
- Audit service
- Important action logging
- Admin/faculty audit view

Exit condition:
- Important workflow actions produce traceable records.

## Phase 10 — UI Polish

- Apply complete theme.
- Improve dashboards.
- Improve tables/forms.
- Add empty states.
- Add validation feedback.
- Add responsive behavior.
- Improve accessibility.

## Phase 11 — Testing & Hardening

- Unit tests
- Repository tests
- Integration tests
- Security tests
- Duplicate concurrency test
- Marks validation tests
- Workflow transition tests

## Phase 12 — Documentation & Demo

Create:
- README
- Architecture diagram
- ER diagram
- Use-case diagram
- Sequence diagrams for request/review
- Setup instructions
- Test evidence
- Demo script
- Viva notes

## Agent Rule

Never skip testing to move to the next phase.

For each phase:

`Inspect → Plan → Implement → Test → Review → Document`

Do not generate the whole project in a single step.
