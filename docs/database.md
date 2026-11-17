# Database Design

## Core Tables

### users

Fields:
- id
- name
- email
- password_hash
- role
- active
- created_at
- updated_at

### exams

Fields:
- id
- name
- subject
- start_date
- end_date
- status
- reevaluation_start
- reevaluation_end
- created_at
- updated_at

The re-evaluation dates may be represented separately or incorporated into an appropriate exam lifecycle model.

### questions

Fields:
- id
- exam_id
- question_text
- max_marks
- created_at
- updated_at

### student_results

Fields:
- id
- student_id
- exam_id
- total_marks
- created_at
- updated_at

Recommended unique relationship:

`UNIQUE(student_id, exam_id)`

### question_marks

Fields:
- id
- student_id
- question_id
- marks_obtained
- created_at
- updated_at

The implementation must ensure that the student/question combination is associated with the same exam through the domain model.

### recheck_requests

Fields:
- id
- student_id
- exam_id
- question_id
- reason
- status
- created_at
- updated_at

Critical constraint:

`UNIQUE(student_id, exam_id, question_id)`

### reviews

Fields:
- id
- request_id
- faculty_id
- decision
- comments
- revised_marks
- reviewed_at

A request can have a review record/history depending on the chosen implementation.

### audit_logs

Fields:
- id
- user_id
- action
- timestamp
- description

---

## Relationships

```text
EXAM 1 ──────< QUESTION

STUDENT 1 ──────< STUDENT_RESULT >────── 1 EXAM

STUDENT 1 ──────< QUESTION_MARK >────── 1 QUESTION

STUDENT 1 ──────< RECHECK_REQUEST >──── 1 EXAM
                           │
                           └──────────── 1 QUESTION

RECHECK_REQUEST 1 ──────< REVIEW >────── FACULTY/USER

USER 1 ──────< AUDIT_LOG
```

## Integrity Rules

1. Every question belongs to one exam.
2. Every student result belongs to one student and one exam.
3. Every question mark references a valid student and question.
4. A re-evaluation request references one student, one exam, and one question.
5. The question in a request must belong to the referenced exam.
6. The student must be associated with the exam.
7. A student may have at most one request for a question in an exam.
8. Revised marks cannot exceed question maximum marks.
9. Audit logs reference the actor responsible for the action where possible.

## Indexes

Consider indexes on:
- users.email
- exams.status
- exams.start_date
- exams.end_date
- questions.exam_id
- student_results.student_id
- student_results.exam_id
- question_marks.student_id
- question_marks.question_id
- recheck_requests.student_id
- recheck_requests.exam_id
- recheck_requests.question_id
- recheck_requests.status
- reviews.request_id
- audit_logs.user_id
- audit_logs.timestamp

## Aggregation

Question request counts can be calculated with:

`COUNT(recheck_requests.id) GROUP BY question_id`

Flag percentage can be calculated as:

`requests_for_question / eligible_students_for_exam * 100`

Do not store derived counts as the only authoritative value.

## Deletion

Avoid hard-deleting records that are required for historical/audit integrity.

For example, a question with requests/reviews should not simply disappear through ordinary CRUD deletion.
