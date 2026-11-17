# Testing Strategy

## Unit Tests

Test:
- Exam state transitions
- Re-evaluation window checks
- Request validation
- Request status transitions
- Revised mark bounds
- Request aggregation
- Threshold calculation
- Turnout/request percentages where applicable

## Repository Tests

Test:
- Unique student/exam/question request constraint
- Request lookup by student
- Request aggregation by question
- Question/exam relationships
- Student/exam relationships
- Review/request relationships

## Integration Tests

Test:
- Login
- Student dashboard
- Exam/question flow
- Marks display
- Request submission
- Faculty review
- Revised marks
- Audit creation

## Security Tests

Test:
- Anonymous → protected route denied
- Student → faculty route denied
- Student → admin route denied
- Student cannot view another student's marks
- Student cannot submit a request for another student
- Faculty/admin authorization works
- CSRF protection works for state-changing forms

## Critical Request Tests

| Scenario | Expected |
|---|---|
| Valid student + valid exam + open period | Request accepted |
| Re-evaluation closed | Rejected |
| Student not associated with exam | Rejected |
| Question belongs to another exam | Rejected |
| Student has no mark for question | Rejected |
| Duplicate request | Rejected |
| Concurrent duplicate requests | At most one persisted |
| Empty reason | Validation failure |
| Excessively long reason | Validation failure |

## Review Tests

| Scenario | Expected |
|---|---|
| Faculty approves request | APPROVED |
| Faculty rejects request | REJECTED |
| Invalid transition | Rejected |
| Revised marks below 0 | Rejected |
| Revised marks above max | Rejected |
| Valid revised marks | Stored |
| Review + mark change | Transactionally consistent |
| Review action | Audit record created |

## Definition of Done

A feature is complete only when:
- Code works.
- Tests exist.
- Tests pass.
- Security boundaries are checked.
- Error states are handled.
- UI follows `theme.md`.
- Documentation matches the implementation.
