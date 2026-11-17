# Project Learning Guide
## Exam Question Re-evaluation & Review Management System

### 1. Welcome to the Platform
This project represents a full-stack, enterprise-grade academic evaluation grievance platform built around Spring Boot 3, Java 21, and Spring Security 6.
Whether you are reviewing this project for academic examination, engineering viva, or software development onboarding, this guide explains how the system works conceptually, architecturally, and practically.

---

### 2. Core Concepts at a Glance

1. **Why Granular Re-evaluation?**
   Traditional systems re-evaluate entire answer booklets, causing immense workload for professors and delays for students. This system breaks examinations down into individual **Questions** and awards **QuestionMarks**, allowing students to dispute specific questions with targeted rationale.

2. **The Three Roles**:
   - **Student**: Views published exam results, drills into question-level mark breakdowns, submits re-evaluation requests during the active window, and tracks request resolution.
   - **Faculty**: Creates exams, configures questions, records student marks, reviews disputed questions, updates marks, and inspects question dispute analytics.
   - **Admin**: Oversees platform integrity, inspects users, monitors system activity, and filters the centralized audit trail.

3. **Key Safeguards**:
   - **Anti-IDOR**: Students can never access or query another student's marks or re-evaluation requests.
   - **Duplicate Request Barrier**: A database composite unique constraint prevents double-submissions for the same question.
   - **Atomic Recalculation**: Approving a re-evaluation updates the question mark and recalculates the student's overall exam result in a single ACID transaction.
   - **Immutable Decisions**: Once a faculty decision is submitted, it cannot be edited or tampered with.

---

### 3. Study Path Recommendation
To thoroughly understand this codebase:
1. Start with [System Overview](../architecture/system-overview.md) and [Layered Architecture](../architecture/layered-architecture.md).
2. Read [Backend Request Lifecycle](backend-request-lifecycle.md) to follow a request from browser to database.
3. Understand the relational model in [Database Design](../architecture/database-design.md).
4. Review security patterns in [Understanding Security](understanding-security.md).
5. Prepare for questions using [Viva & Interview Preparation](viva-preparation.md).
