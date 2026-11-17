# Route / Application Contract

The application is primarily server-rendered with Thymeleaf. These routes define the intended application boundaries.

## Authentication

### GET `/login`
Show login form.

### POST `/login`
Authenticate user.

### POST `/logout`
Log out.

## Student

### GET `/student/dashboard`
Student dashboard.

### GET `/student/exams`
List exams available to the student.

### GET `/student/exams/{examId}`
View exam result/question marks.

### GET `/student/exams/{examId}/questions/{questionId}/request`
Show re-evaluation form.

### POST `/student/exams/{examId}/questions/{questionId}/request`
Submit re-evaluation request.

The student identity must come from the authenticated principal.

### GET `/student/requests`
List current student's requests.

### GET `/student/requests/{requestId}`
View request details/status.

## Faculty

### GET `/faculty/dashboard`
Faculty dashboard.

### GET `/faculty/exams`
Manage/view exams.

### GET `/faculty/exams/new`
Create exam form.

### POST `/faculty/exams`
Create exam.

### GET `/faculty/exams/{examId}/questions`
Manage questions.

### POST `/faculty/exams/{examId}/questions`
Create question.

### GET `/faculty/exams/{examId}/marks`
Manage marks.

### POST `/faculty/exams/{examId}/reevaluation/open`
Open re-evaluation.

### POST `/faculty/exams/{examId}/reevaluation/close`
Close re-evaluation.

### GET `/faculty/requests`
View requests.

### GET `/faculty/requests/{requestId}`
Review request.

### POST `/faculty/requests/{requestId}/review`
Submit decision/comments/revised marks.

### GET `/faculty/analytics`
View question-wise request analytics.

## Admin

### GET `/admin/dashboard`
Administrative dashboard.

### GET `/admin/students`
Manage students.

### GET `/admin/audit-logs`
View audit logs.

Additional admin routes should be introduced only when supported by the requirements.

## Error Responses

For server-rendered pages:
- 401 → authentication/login
- 403 → forbidden
- 404 → not found
- 409 → business conflict
- 422 → validation error
- 500 → generic server error

Never expose stack traces to users.
