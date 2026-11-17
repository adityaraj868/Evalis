# Database Constraints & Indexing Strategy
## Exam Question Re-evaluation & Review Management System

### 1. Integrity Constraints Strategy
The database relies on explicit constraints to enforce data integrity at the lowest physical storage layer, preventing software bugs, concurrency races, or administrative scripts from corrupting state.

#### 1.1 Unique Constraints

| Table | Constraint Name | Columns | Architectural Rationale |
|---|---|---|---|
| `users` | `uk_users_email` | `email` | Ensures email addresses serve as unique user logins. |
| `questions` | `uk_exam_question_number` | `(exam_id, question_number)` | Prevents duplicate question numbering within the same exam. |
| `student_results` | `uk_student_exam_result` | `(student_id, exam_id)` | Prevents duplicate summary result records for a student in an exam. |
| `question_marks` | `uk_student_question_mark` | `(student_id, question_id)` | Guarantees exactly one mark entry per student per question. |
| `recheck_requests` | `uk_student_exam_question_recheck` | `(student_id, exam_id, question_id)` | **Mission Critical**: Prevents a student from submitting duplicate concurrent re-evaluation requests for the same question. |
| `reviews` | `uk_review_request` | `request_id` | Guarantees that a re-evaluation request has exactly one faculty review. |

---

### 2. Physical Indexing Strategy

Indexes are placed selectively to accelerate search and filtering operations while minimizing overhead during bulk write transactions (e.g. batch marks entry).

#### 2.1 Index Details

1. **`users(email)`**:
   - Unique B-tree index.
   - Purpose: Makes user authentication lookup $O(\log N)$ on every login attempt.

2. **`audit_logs(action)`**:
   - Non-unique B-tree index.
   - Purpose: Speeds up administrative filtering by action type (e.g., `REVIEW_COMPLETED`, `REQUEST_SUBMITTED`).

3. **`audit_logs(resource_type, resource_id)`**:
   - Composite B-tree index.
   - Purpose: Accelerates retrieval of historical audit logs for a specific entity (e.g. all changes to `RecheckRequest #14`).

4. **`audit_logs(timestamp)`**:
   - Non-unique B-tree index.
   - Purpose: Orders audit trail entries chronologically in descending order for the admin dashboard.

5. **`recheck_requests(student_id, exam_id, question_id)`**:
   - Composite Unique Index.
   - Purpose: Dual role—serves as the uniqueness constraint and provides fast lookups when verifying if a request already exists.
