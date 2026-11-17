# Transaction Management & ACID Guarantees
## Exam Question Re-evaluation & Review Management System

### 1. Transaction Boundaries & Declarative `@Transactional`
In a grade re-evaluation platform, partial updates pose severe integrity risks (e.g., updating a question's marks without recalculating the student's total result, or recording a review without updating the request status). 

To ensure **Atomicity, Consistency, Isolation, and Durability (ACID)**, the platform uses Spring's declarative transaction management (`@Transactional`) configured on all mutating service methods.

---

### 2. Critical Transaction Scenarios

#### Scenario 1: Faculty Review Adjudication & Grade Synchronization
When a faculty member approves a dispute:
```
[BEGIN TRANSACTION]
  1. Retrieve RecheckRequest (verify status in SUBMITTED or UNDER_REVIEW)
  2. Insert Review record (facultyId, decision=APPROVED, revisedMarks, comments)
  3. Update RecheckRequest status = APPROVED
  4. Update QuestionMark (set marksObtained = revisedMarks)
  5. Recalculate StudentResult (sum all QuestionMarks for this student and exam)
  6. Update StudentResult (set totalMarks = sum)
  7. Insert AuditLog (action=REVIEW_COMPLETED, metadata, actor)
[COMMIT TRANSACTION]
```
If any step fails (e.g. database timeout or validation failure on revised marks), Spring's `TransactionInterceptor` catches the exception and commands the underlying JDBC connection to execute `ROLLBACK`. No partial state or stale total marks can leak into the database.

#### Scenario 2: Batch Student Marks Recording
In `MarksService.recordExamMarksForStudent(...)`:
- Multiple question marks are validated against their respective `maxMarks`.
- If even one score in the batch exceeds `maxMarks` or is negative, a `ValidationException` is thrown before or during persistence.
- The transaction rolls back completely, ensuring no student is left with half-recorded scores.

---

### 3. Isolation Levels and Read Optimizations
- **Default Isolation Level**: `ISOLATION_DEFAULT` (maps to `READ_COMMITTED` in MySQL and H2), which prevents dirty reads while maximizing throughput.
- **Read-Only Transactions**: Read methods are annotated with `@Transactional(readOnly = true)`. This hints to Hibernate to skip dirty checking on loaded entities, saving CPU cycles and memory.
- **Race Condition Prevention**: Concurrent duplicate submissions for the same question fail cleanly against the database-level unique constraint, throwing a `DataIntegrityViolationException` that rolls back the active transaction and returns a 400 Bad Request to the client.
