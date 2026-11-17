# Database Design & Architecture
## Exam Question Re-evaluation & Review Management System

### 1. Database Architecture Overview
The system relies on an ACID-compliant relational database (H2 In-Memory for testing and rapid local execution; MySQL 8.0 for production). 
The schema consists of 8 core tables normalized to Third Normal Form (3NF), ensuring data integrity, elimination of update anomalies, and referential safety.

---

### 2. Entity-Relationship Overview

```
+---------------+          1:N          +-------------------+
|     USERS     |---------------------->|   STUDENT_RESULTS |
| (Students,    |                       +-------------------+
|  Faculty,     |                                 |
|  Admins)      |          1:N                    | 1:N
+---------------+---------------------+           v
   |         |                        |  +-------------------+
   | 1:N     | 1:N                    |  |   QUESTION_MARKS  |
   |         v                        |  +-------------------+
   |  +---------------+               |           ^
   |  |  AUDIT_LOGS   |               |           |
   |  +---------------+               |           |
   v                                  v           | 1:N
+---------------+          1:N        +-----------------------+
|     EXAMS     |-------------------->|       QUESTIONS       |
+---------------+                     +-----------------------+
   |                                              ^
   | 1:N                                          |
   v                                              | 1:N
+-------------------------------------------------------------+
|                      RECHECK_REQUESTS                       |
|   UNIQUE(student_id, exam_id, question_id)                  |
+-------------------------------------------------------------+
   |
   | 1:1
   v
+---------------+
|    REVIEWS    |
+---------------+
```

---

### 3. Table Schema & Key Specifications

#### 3.1 `users`
Represents all system actors.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `name` (VARCHAR(100), NOT NULL)
- `email` (VARCHAR(120), UNIQUE, NOT NULL, INDEXED)
- `password_hash` (VARCHAR(255), NOT NULL)
- `role` (VARCHAR(20), NOT NULL: `STUDENT`, `FACULTY`, `ADMIN`)
- `active` (BOOLEAN, DEFAULT TRUE)
- `created_at`, `updated_at` (TIMESTAMP)

#### 3.2 `exams`
Defines an examination event and its re-evaluation timeline.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `name` (VARCHAR(150), NOT NULL)
- `subject` (VARCHAR(100), NOT NULL)
- `status` (VARCHAR(30), NOT NULL: `DRAFT`, `PUBLISHED`, `RE_EVALUATION_OPEN`, `RE_EVALUATION_CLOSED`, `ARCHIVED`)
- `start_date`, `end_date` (TIMESTAMP)
- `reevaluation_start`, `reevaluation_end` (TIMESTAMP)
- `created_at`, `updated_at` (TIMESTAMP)

#### 3.3 `questions`
Question definitions linked to an exam.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `exam_id` (BIGINT, FK -> exams.id, NOT NULL)
- `question_number` (INT, NOT NULL)
- `question_text` (TEXT, NOT NULL)
- `max_marks` (DOUBLE, NOT NULL)
- Constraint: `UNIQUE(exam_id, question_number)`

#### 3.4 `student_results`
Stores the overall aggregate score and grading for a student in an exam.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `student_id` (BIGINT, FK -> users.id, NOT NULL)
- `exam_id` (BIGINT, FK -> exams.id, NOT NULL)
- `total_marks` (DOUBLE, NOT NULL)
- `grade` (VARCHAR(10))
- Constraint: `UNIQUE(student_id, exam_id)`

#### 3.5 `question_marks`
Granular question-level marks for each student.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `student_id` (BIGINT, FK -> users.id, NOT NULL)
- `question_id` (BIGINT, FK -> questions.id, NOT NULL)
- `marks_obtained` (DOUBLE, NOT NULL)
- `remarks` (VARCHAR(255))
- Constraint: `UNIQUE(student_id, question_id)`

#### 3.6 `recheck_requests`
Granular re-evaluation requests submitted by students.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `student_id` (BIGINT, FK -> users.id, NOT NULL)
- `exam_id` (BIGINT, FK -> exams.id, NOT NULL)
- `question_id` (BIGINT, FK -> questions.id, NOT NULL)
- `reason` (TEXT, NOT NULL)
- `status` (VARCHAR(30), NOT NULL: `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`)
- Constraint: `UNIQUE(student_id, exam_id, question_id)` (Crucial duplicate prevention constraint)

#### 3.7 `reviews`
Faculty decision records for recheck requests.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `request_id` (BIGINT, FK -> recheck_requests.id, UNIQUE, NOT NULL)
- `faculty_id` (BIGINT, FK -> users.id, NOT NULL)
- `decision` (VARCHAR(20), NOT NULL: `APPROVED`, `REJECTED`)
- `revised_marks` (DOUBLE)
- `comments` (TEXT, NOT NULL)
- `reviewed_at` (TIMESTAMP, NOT NULL)

#### 3.8 `audit_logs`
System-wide immutable audit trail.
- `id` (BIGINT, PK, AUTO_INCREMENT)
- `user_id` (BIGINT, FK -> users.id, NULLABLE for system actions)
- `action` (VARCHAR(60), NOT NULL, INDEXED)
- `resource_type` (VARCHAR(50), INDEXED)
- `resource_id` (BIGINT, INDEXED)
- `previous_value` (TEXT)
- `updated_value` (TEXT)
- `description` (TEXT)
- `timestamp` (TIMESTAMP, NOT NULL, INDEXED)
