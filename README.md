# Exam Question Re-evaluation & Review Management System

A secure, enterprise-grade academic management platform built with **Spring Boot 3**, **Java 21 LTS**, **Spring Security 6**, and **Thymeleaf** that digitizes the university post-examination grievance redressal and question-level re-evaluation workflow.

---

## 1. System Overview & Problem Statement

In conventional academic environments, post-examination evaluation appeals require students to dispute an entire paper via manual paper-based forms. This creates substantial delays, administrative friction, lack of transparency, and heavy faculty workloads.

This platform introduces **granular question-level re-evaluation**:
- **Students** view question-wise marks breakdowns and dispute specific questions with academic justifications during an active re-evaluation window.
- **Faculty** manage exam lifecycles, configure questions, record batch scores, review student disputes, award revised marks with atomic score recalculation, and inspect question dispute analytics.
- **Administrators** monitor system security, manage users, and inspect an immutable centralized audit trail.

---

## 2. Core Workflow

```
Exam Creation (DRAFT) 
  → Question Configuration & Publication (PUBLISHED)
  → Student Batch Marks Recorded
  → Re-evaluation Window Opens (RE_EVALUATION_OPEN)
  → Student Submits Question-Level Request (SUBMITTED)
  → Faculty Opens Request (UNDER_REVIEW)
  → Faculty Adjudication (APPROVED / REJECTED)
  → Atomic Grade Recalculation & Immutable Review Saved
  → Structured Audit Log Recorded
```

---

## 3. Technology Stack

- **Runtime**: Java OpenJDK 21 LTS
- **Backend Framework**: Spring Boot 3.4.3 (Jakarta EE 10 baseline)
- **Security**: Spring Security 6.4.x (Session-based RBAC, BCrypt password hashing, CSRF protection, `@EnableMethodSecurity`)
- **Data Persistence**: Spring Data JPA & Hibernate ORM 6.6.8.Final
- **Relational Databases**: 
  - H2 In-Memory (Zero-configuration testing and dev profile)
  - MySQL 8.0 (Production profile)
- **Connection Pooling**: HikariCP 5.1.x
- **Presentation**: Server-Side Rendering via Thymeleaf 3.1.x with Spring Security Dialect
- **Styling**: Bootstrap 5.3.x responsive layout
- **Testing**: JUnit 5 (Jupiter), AssertJ, Mockito, Spring Test (MockMvc)
- **Build Tool**: Apache Maven 3.9+

---

## 4. Implementation Status (Phases 0 to 9 Completed)

| Phase | Title | Scope & Delivered Features | Status |
|---|---|---|---|
| **Phase 0** | Project Bootstrap | Spring Boot 3.4.3 setup, Maven POM, layouts, and baseline context. | `COMPLETED` |
| **Phase 1** | Domain Model & Relational Schema | 8 JPA entities, 4 enums, composite unique constraints, 8 repositories. | `COMPLETED` |
| **Phase 2** | Authentication & Authorization | RBAC (`STUDENT`, `FACULTY`, `ADMIN`), method security, Anti-IDOR, custom 400/403/404 error handlers. | `COMPLETED` |
| **Phase 3** | Examination & Question Management | Exam state machine (`DRAFT` → `PUBLISHED` → `OPEN` → `CLOSED` → `ARCHIVED`), question immutability. | `COMPLETED` |
| **Phase 4** | Marks Management | Question-level marks recording, bounds checking, atomic total marks recalculation. | `COMPLETED` |
| **Phase 5** | Re-evaluation Request Core | Submissions, window verification, composite uniqueness enforcement (`student_id, exam_id, question_id`). | `COMPLETED` |
| **Phase 6** | Request Tracking | Status progression (`SUBMITTED` → `UNDER_REVIEW`), student tracking portal, audit emission. | `COMPLETED` |
| **Phase 7** | Faculty Review Workflow | Review adjudication (`APPROVED`/`REJECTED`), atomic score harmonization, decision immutability. | `COMPLETED` |
| **Phase 8** | Question-wise Analytics | Single-query dispute aggregation, dispute threshold alerts, zero-division protection. | `COMPLETED` |
| **Phase 9** | Centralized Audit Trail | Structured audit logging (`resourceType`, `resourceId`, `previousValue`, `updatedValue`), multi-criteria filtering. | `COMPLETED` |

---

## 5. Getting Started

### 5.1 Prerequisites
- **Java Development Kit (JDK)**: OpenJDK 21 or higher
- **Build Tool**: Apache Maven 3.8+ (or bundled wrapper)
- **Git**

### 5.2 Running the Application Locally

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Enterprise
   ```

2. **Run using Maven with the default profile (H2 in-memory DB)**:
   ```bash
   mvn spring-boot:run
   ```
   *The application will start on port `8080` and populate initial seed data automatically.*

3. **Open in Browser**:
   ```
   http://localhost:8080
   ```

### 5.3 Default Seed Credentials

| Role | Email Address | Password | Landing Page |
|---|---|---|---|
| **Student** | `student1@example.com` | `password` | `/student/dashboard` |
| **Student** | `student2@example.com` | `password` | `/student/dashboard` |
| **Faculty** | `faculty1@example.com` | `password` | `/faculty/dashboard` |
| **Admin** | `admin@example.com` | `password` | `/admin/dashboard` |

---

## 6. Running Automated Tests

The application includes a comprehensive automated test suite consisting of **67 tests** across **11 test classes** verifying unit, repository, service integration, and security layers:

```bash
mvn clean test
```

### Test Suite Summary:
- `SecurityAccessTests`: Role-based access control, unauthenticated redirects, anti-IDOR tests.
- `ExamLifecycleTests`: Examination state machine transitions, question immutability, date bounds.
- `MarksManagementTests`: Bounds validation, batch recording, automatic score recalculation.
- `RecheckRequestCoreTests`: Multi-tier validation, window checking, composite duplicate rejection.
- `RequestTrackingTests`: Status progression to `UNDER_REVIEW`, student tracking views.
- `FacultyReviewWorkflowTests`: Decision immutability, revised score sync, rejection handling.
- `QuestionAnalyticsTests`: Dispute frequency calculation, threshold alerts, zero-division safety.
- `AuditTrailTests`: Structured audit logging, multi-criteria filtering, `@EntityGraph` query tests.
- `DomainRepositoryTests`: JPA mapping, cascade deletes, database constraints.

---

## 7. Technical Documentation Directory

Comprehensive architectural deep-dives and guides are located in the [`docs/`](docs/) directory:

- [Technical Documentation Index](docs/README.md)
- **Architecture**:
  - [System Overview](docs/architecture/system-overview.md)
  - [Layered Architecture](docs/architecture/layered-architecture.md)
  - [Component Interactions](docs/architecture/component-interactions.md)
  - [Database Design](docs/architecture/database-design.md)
  - [Authentication Flow](docs/architecture/authentication-flow.md)
  - [Authorization Flow & Anti-IDOR](docs/architecture/authorization-flow.md)
  - [Examination Workflow](docs/architecture/examination-workflow.md)
  - [Re-evaluation Workflow](docs/architecture/reevaluation-workflow.md)
  - [Architecture Decision Records (ADRs)](docs/architecture/architecture-decisions.md)
- **Technology & Database**:
  - [Technology Stack](docs/technology/technology-stack.md)
  - [Technology Explanations](docs/technology/technology-explanations.md)
  - [Relational Schema (DDL)](docs/database/schema.md)
  - [Relationships & Multiplicities](docs/database/relationships.md)
  - [Constraints & Indexes](docs/database/constraints-and-indexes.md)
  - [Transaction Management](docs/database/transaction-management.md)
- **Testing & Quality**:
  - [Testing Strategy](docs/testing/testing-strategy.md)
  - [Test Cases Specification](docs/testing/test-cases.md)
  - [Test Results](docs/testing/test-results.md)
- **Learning & Viva Preparation**:
  - [Project Learning Guide](docs/learning/project-learning-guide.md)
  - [Backend Request Lifecycle](docs/learning/backend-request-lifecycle.md)
  - [Understanding the Architecture](docs/learning/understanding-the-architecture.md)
  - [Understanding Database Design](docs/learning/understanding-database-design.md)
  - [Understanding Security](docs/learning/understanding-security.md)
  - [Viva & Interview Preparation](docs/learning/viva-preparation.md)
- **Diagrams**:
  - [System Architecture Diagram](docs/diagrams/system-architecture.md)
  - [Entity Relationship Diagram](docs/diagrams/entity-relationship.md)
  - [UML Class Diagram](docs/diagrams/class-diagram.md)
  - [UML Use Case Diagram](docs/diagrams/use-case-diagram.md)
  - [Activity Diagrams](docs/diagrams/activity-diagrams.md)
  - [Sequence Diagrams](docs/diagrams/sequence-diagrams.md)
  - [State Diagrams](docs/diagrams/state-diagrams.md)
