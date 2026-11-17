# Exam Re-evaluation System — Antigravity Workspace Rules

Apply these rules to all project work.

## Source Documents

Before substantial implementation, read:
- `requirements.md`
- `architecture.md`
- `database.md`
- `security.md`
- `workflow.md`
- `theme.md`
- `implementation-plan.md`
- `testing.md`

The uploaded project proposal is the functional source of truth when these documents need interpretation.

## Technology

Use:
- Java 21
- Spring Boot
- Spring Security
- Spring Data JPA / Hibernate
- MySQL
- Thymeleaf
- HTML/CSS/JavaScript
- Maven
- JUnit 5

Do not add Redis or another database in the baseline.

## Architecture

Use a modular monolith.

Preferred flow:

`Thymeleaf → Controller → Service → Repository → MySQL`

Controllers stay thin.

Business rules belong in services/domain logic.

## Critical Business Rules

1. Student identity comes from the authenticated principal.
2. Never trust browser-supplied student IDs.
3. Server decides whether re-evaluation is open.
4. Question must belong to the exam.
5. Student must be associated with the exam.
6. Student must have a valid mark for the question.
7. Duplicate request prevention must exist at application and database levels.
8. Database must enforce:
   `UNIQUE(student_id, exam_id, question_id)`
9. Handle concurrent duplicate submissions safely.
10. Revised marks must be within `[0, question.maxMarks]`.
11. Faculty retains final review authority.
12. Important actions must be auditable.
13. Historical/audit integrity must not be destroyed by casual CRUD deletion.

## Security

Use Spring Security.

Do not rely on:
- Hidden fields
- Disabled buttons
- Client-side JavaScript
- URL obscurity

for authorization.

Keep CSRF enabled for Thymeleaf forms.

Never log or commit secrets.

## Scope

Do not introduce:
- Blockchain
- Biometrics
- Facial recognition
- Microservices
- Kubernetes
- Online exam conduction
- Automatic answer evaluation
- OCR
- AI grading

unless explicitly requested.

## UI

Follow `theme.md`.

Do not create separate visual systems for different pages.

Reuse shared fragments/components.

## Development Workflow

For non-trivial tasks:

`Inspect → Plan → Implement → Test → Review → Report`

Before editing:
- Inspect relevant existing code.
- Identify affected files.
- State the intended change.

After editing:
- Run relevant tests.
- Compile/build.
- Review changed files/diff.
- Update documentation when behavior changes.

Do not silently change requirements.

Do not create hundreds of speculative files.

Do not use placeholder implementations merely to make the application appear complete.
