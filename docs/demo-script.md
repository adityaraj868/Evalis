# Demo Script

## 1. Login

Show the login page.

Demonstrate:
- Student login
- Faculty login
- Role-based access

## 2. Faculty Creates Examination

Create:

`Data Structures Mid-Semester Examination`

Add several questions and maximum marks.

## 3. Enter Marks

Use example data:

```text
Q1  8/10
Q2  3/10
Q3  9/10
Q4  2/10
Q5 10/10
```

## 4. Open Re-evaluation

Show that the re-evaluation period is open.

## 5. Student Request

Login as a student.

Open the exam.

Select Q4.

Enter a reason such as:
`My solution contains the required approach, but I believe insufficient marks were awarded.`

Submit.

## 6. Duplicate Request

Attempt to submit Q4 again.

Expected:
`A re-evaluation request already exists for this question.`

Explain that both application validation and the database unique constraint prevent duplicates.

## 7. Faculty Dashboard

Show question-wise counts.

Example:

```text
Q1 → 5
Q2 → 12
Q3 → 4
Q4 → 67
Q5 → 3
```

Show Q4 as a high-demand/flagged question if threshold functionality is enabled.

## 8. Faculty Review

Open Q4 requests.

Review reasons.

Approve a request.

Record revised marks, for example:

`2/10 → 7/10`

## 9. Audit

Show that the review/mark-change action created an audit record.

## 10. Student Tracking

Return to student account.

Show:
- Request status
- Faculty decision
- Revised marks

## 11. Security Demo

Attempt to open a faculty/admin page as a student.

Expected:
`403 Forbidden / Access Denied`

## 12. Architecture Explanation

Explain:

`Thymeleaf → Controller → Service → Repository → MySQL`

and emphasize:
- Spring Security
- JPA/Hibernate
- Database constraints
- Transactional workflow
- Audit logging
