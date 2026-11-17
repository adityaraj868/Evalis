# Security Requirements

## Authentication

Use Spring Security.

Passwords must be stored using a strong password hashing mechanism such as BCrypt/Argon2 supported by the selected Spring Security version.

Never store plaintext passwords.

## Roles

Required roles:

```text
STUDENT
FACULTY
ADMIN
```

## Authorization

Server-side authorization must protect:
- Faculty dashboards
- Admin functions
- Marks management
- Review decisions
- Audit logs

Do not use frontend hiding as a security mechanism.

## Student Identity

For student operations, derive the student identity from the authenticated principal.

Never trust a `studentId` supplied by the browser as proof of identity.

## IDOR Prevention

A student must not be able to:
- View another student's marks.
- View another student's requests.
- Submit a request on behalf of another student.
- Access faculty/admin data.

Changing an ID in the URL must not bypass authorization.

## Re-evaluation Security

Before creating a request, verify server-side:
- authenticated student
- exam eligibility
- re-evaluation period
- question/exam relationship
- question mark existence
- duplicate request state

## Duplicate Requests

Use both:
- Application validation for a good user experience.
- Database unique constraint for final integrity.

Constraint:

`UNIQUE(student_id, exam_id, question_id)`

Handle concurrent duplicate insert attempts as a controlled conflict.

## Revised Marks Security

Only authorized faculty/admin users may modify revised marks.

Validate:
- request exists
- request belongs to correct exam/question
- revised marks are within bounds
- request is in a state that permits review/update

## CSRF

Keep CSRF protection enabled for Thymeleaf browser forms.

All state-changing requests must use the standard Spring Security CSRF mechanism.

## Input Validation

Validate:
- Email
- Names
- Question text
- Subject
- Dates
- Reasons
- Comments
- Marks
- IDs
- State transitions

Never rely exclusively on client-side validation.

## Session Security

Use Spring Security's secure session handling:
- Session fixation protection
- Logout invalidation
- HttpOnly cookies
- Secure cookies when HTTPS is used
- Appropriate SameSite policy

## Logging

Do not log:
- Passwords
- Session tokens
- CSRF tokens
- Authentication secrets

Audit important business actions, but avoid recording unnecessary sensitive information.

## Secrets

Never commit:
- Database passwords
- API keys
- Private keys
- Secret environment files

Use environment variables/local untracked configuration.

## Security Tests

At minimum test:
- Anonymous user accessing protected pages
- Student accessing faculty/admin routes
- Faculty accessing unauthorized admin-only operations if applicable
- Student viewing another student's marks
- Student submitting for another student
- Invalid exam/question combinations
- Closed re-evaluation period
- Duplicate request
- Invalid revised marks
