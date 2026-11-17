# Architecture Decisions

## ADR-001: Modular Monolith

### Decision
Use one Spring Boot application with layered modules.

### Reason
The project is a three-member semester project. A monolith is easier to implement, test, deploy, and explain.

## ADR-002: MySQL as Source of Truth

### Decision
Use MySQL for exams, marks, requests, reviews, and audit records.

### Reason
The application requires relational integrity, transactions, joins, and database constraints.

## ADR-003: Database-Level Duplicate Prevention

### Decision
Enforce:

`UNIQUE(student_id, exam_id, question_id)`

on re-evaluation requests.

### Reason
Application-only duplicate checks can fail under concurrent submissions.

## ADR-004: Server-Side Workflow Validation

### Decision
The backend decides whether a request is allowed.

### Reason
Browser-side controls can be bypassed.

## ADR-005: Faculty Final Authority

### Decision
The system assists faculty by aggregating and organizing requests but does not automatically decide whether a student's answer deserves more marks.

### Reason
This matches the project proposal and keeps the system a review-management platform rather than an automated grading system.

## ADR-006: Thymeleaf

### Decision
Use Thymeleaf with Spring Boot rather than a separate SPA.

### Reason
It keeps the project focused on Java/Spring enterprise development and reduces unnecessary frontend/backend complexity.

## ADR-007: No Redis in Baseline

### Decision
Do not include Redis initially.

### Reason
The current project scope is already substantial. Caching is not required for correctness or normal college-scale usage.
