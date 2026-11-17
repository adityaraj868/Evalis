# Business Workflows

## 1. Exam Setup

```text
Faculty/Admin
   ↓
Create Exam
   ↓
Add Questions
   ↓
Enter/Upload Marks
   ↓
Publish Exam
   ↓
Open Re-evaluation Period
```

## 2. Student Re-evaluation

```text
Student Login
   ↓
Dashboard
   ↓
Select Exam
   ↓
View Question-wise Marks
   ↓
Select Question
   ↓
Enter Reason
   ↓
Submit
   ↓
Server Validation
   ↓
Store Request
```

## 3. Validation

```text
Authenticated?
   ↓ yes
Student belongs to exam?
   ↓ yes
Re-evaluation open?
   ↓ yes
Question belongs to exam?
   ↓ yes
Question mark exists?
   ↓ yes
Already requested?
   ↓ no
Create request
```

Any failed condition must reject the request.

## 4. Aggregation

```text
Requests
   ↓
Group by Question
   ↓
Calculate Count
   ↓
Calculate Percentage if enabled
   ↓
Apply Threshold if enabled
   ↓
Faculty Dashboard
```

## 5. Faculty Review

```text
Faculty Dashboard
   ↓
Question / Request
   ↓
Inspect student reason(s)
   ↓
Review
   ↓
Approve or Reject
   ↓
Optional revised marks
   ↓
Comments
   ↓
Audit
   ↓
Complete
```

## 6. Request State Lifecycle

```text
SUBMITTED
    ↓
UNDER_REVIEW
    ├──→ APPROVED
    │       ↓
    │   COMPLETED
    │
    └──→ REJECTED
            ↓
        COMPLETED
```

## 7. Mark Revision

If approved:

```text
Review
  ↓
Validate revised marks
  ↓
Update question mark
  ↓
Record review
  ↓
Create audit event
  ↓
Update student-visible result
```

The system must never allow revised marks above the question's maximum.

## 8. Audit Workflow

Important actions create records:

```text
Actor
 ↓
Action
 ↓
Timestamp
 ↓
Description
 ↓
Audit Log
```
