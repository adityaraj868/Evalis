# Exam Question Re-evaluation & Review Management System

A secure web-based academic management system that digitizes the examination question re-evaluation workflow.

## Core Workflow

`Exam Setup → Marks Published → Re-evaluation Opens → Student Requests → Validation → Question-wise Aggregation → Faculty Review → Decision → Revised Marks → Audit`

## Primary Users

- STUDENT
- FACULTY
- ADMIN

The uploaded project proposal defines students, faculty, and administrators as the target users and specifies Java, Spring Boot, Spring Security, Thymeleaf, Hibernate/JPA, and MySQL as the primary stack. See the source proposal, pages 1–2.

## Current Technology Stack

- Java 21
- Spring Boot
- Spring Security
- Spring Data JPA / Hibernate
- MySQL
- Thymeleaf
- HTML/CSS/JavaScript
- Maven
- JUnit 5
- Git/GitHub

Do not add Redis, MongoDB, microservices, Docker/Kubernetes, blockchain, biometrics, or other infrastructure unless explicitly approved later.

## Source of Truth

The uploaded semester project proposal is the functional baseline. The files in this repository translate that proposal into implementation-oriented requirements and agent instructions.

## Critical Integrity Rules

- A student can request re-evaluation only for an eligible exam/question.
- A student cannot request the same question twice for the same exam.
- The database must enforce the uniqueness of `(student_id, exam_id, question_id)`.
- Faculty retains final authority over review decisions.
- Revised marks must be validated against the question's maximum marks.
- Important actions must create audit records.
- Server-side validation is authoritative.

## Antigravity Context

Read these before substantial implementation:

- `requirements.md`
- `theme.md`
- `architecture.md`
- `database.md`
- `security.md`
- `workflow.md`
- `api.md`
- `implementation-plan.md`
- `testing.md`
- `.agents/rules/project-rules.md`

Do not implement the entire application in one pass. Work milestone by milestone.
