# Exam Question Re-evaluation & Review Management System
## Technical Documentation Index

Welcome to the comprehensive technical documentation for the **Exam Question Re-evaluation & Review Management System**. This documentation is tailored to provide an in-depth understanding of the system's architecture, technologies, database design, backend implementation phases, testing results, and system design diagrams.

---

## Documentation Structure

### 1. Architecture (`docs/architecture/`)
- [System Overview](file:///home/epsilon/clg/Enterprise/docs/architecture/system-overview.md): High-level system architecture and architectural philosophy.
- [Layered Architecture](file:///home/epsilon/clg/Enterprise/docs/architecture/layered-architecture.md): Presentation, Business Logic, Data Access, and Database layer boundaries.
- [Component Interactions](file:///home/epsilon/clg/Enterprise/docs/architecture/component-interactions.md): Interactions between Controllers, Services, Repositories, and Entities.
- [Database Design](file:///home/epsilon/clg/Enterprise/docs/architecture/database-design.md): Relational schema, normalization, and integrity design.
- [Authentication Flow](file:///home/epsilon/clg/Enterprise/docs/architecture/authentication-flow.md): Custom UserDetailsService, BCrypt hashing, and role-based redirect handler.
- [Authorization Flow](file:///home/epsilon/clg/Enterprise/docs/architecture/authorization-flow.md): Role-based access control, `@EnableMethodSecurity`, and IDOR defenses.
- [Examination Workflow](file:///home/epsilon/clg/Enterprise/docs/architecture/examination-workflow.md): Examination lifecycle state machine (`DRAFT` → `PUBLISHED` → `RE_EVALUATION_OPEN` → `CLOSED` → `ARCHIVED`).
- [Re-evaluation Workflow](file:///home/epsilon/clg/Enterprise/docs/architecture/reevaluation-workflow.md): Request submission, window verification, faculty review, score amendment, and audit logging.
- [Architecture Decisions](file:///home/epsilon/clg/Enterprise/docs/architecture/architecture-decisions.md): Architecture Decision Records (ADRs 001 through 007).

### 2. Technology (`docs/technology/`)
- [Technology Stack](file:///home/epsilon/clg/Enterprise/docs/technology/technology-stack.md): Verified technology stack, versions, and build tooling.
- [Technology Explanations](file:///home/epsilon/clg/Enterprise/docs/technology/technology-explanations.md): Deep-dive explanations of Spring Boot, Spring MVC, Spring Security, Hibernate ORM, Thymeleaf, and Maven.

### 3. Database (`docs/database/`)
- [Schema Specification](file:///home/epsilon/clg/Enterprise/docs/database/schema.md): Complete DDL specifications for all 8 application tables.
- [Relationships & Cardinality](file:///home/epsilon/clg/Enterprise/docs/database/relationships.md): Entity relationship mappings, foreign keys, and fetch strategies.
- [Constraints and Indexes](file:///home/epsilon/clg/Enterprise/docs/database/constraints-and-indexes.md): Primary keys, composite unique constraints (`UNIQUE(student_id, exam_id, question_id)`), and query performance indexes.
- [Transaction Management](file:///home/epsilon/clg/Enterprise/docs/database/transaction-management.md): ACID guarantees, `@Transactional` boundaries, and rollback rules.

### 4. Implementation Phases (`docs/implementation/`)
- [Initial Codebase Audit](file:///home/epsilon/clg/Enterprise/docs/implementation/initial-codebase-audit.md): Complete baseline technical audit.
- [Phase Progress Tracker](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-progress.md): Roadmap tracking status across all phases.
- [Phase 2: Authentication & Authorization](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-2.md)
- [Phase 3: Examination & Question Management](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-3.md)
- [Phase 4: Marks Management](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-4.md)
- [Phase 5: Re-evaluation Request Core](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-5.md)
- [Phase 6: Request Tracking](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-6.md)
- [Phase 7: Faculty Review Workflow](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-7.md)
- [Phase 8: Question-wise Analytics](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-8.md)
- [Phase 9: Centralized Audit Trail](file:///home/epsilon/clg/Enterprise/docs/implementation/phase-9.md)

### 5. Testing & Quality Assurance (`docs/testing/`)
- [Testing Strategy](file:///home/epsilon/clg/Enterprise/docs/testing/testing-strategy.md): Unit, integration, security, boundary, and repository testing methodology.
- [Test Cases](file:///home/epsilon/clg/Enterprise/docs/testing/test-cases.md): Granular specification of all 58 automated test cases.
- [Test Results](file:///home/epsilon/clg/Enterprise/docs/testing/test-results.md): Execution logs and verification metrics across 11 test suites.

### 6. Learning & Viva Preparation (`docs/learning/`)
- [Project Learning Guide](file:///home/epsilon/clg/Enterprise/docs/learning/project-learning-guide.md): High-yield conceptual walkthrough for students and backend engineers.
- [Backend Request Lifecycle](file:///home/epsilon/clg/Enterprise/docs/learning/backend-request-lifecycle.md): Tracing HTTP requests from TCP socket to MySQL row mutation.
- [Understanding the Architecture](file:///home/epsilon/clg/Enterprise/docs/learning/understanding-the-architecture.md): Why Modular Monolith? SOLID, DRY, and design patterns used.
- [Understanding Database Design](file:///home/epsilon/clg/Enterprise/docs/learning/understanding-database-design.md): 3NF normalization, foreign key cascading, and concurrency protection.
- [Understanding Security](file:///home/epsilon/clg/Enterprise/docs/learning/understanding-security.md): Spring Security filter chain internals, BCrypt salt hashing, CSRF, and IDOR prevention.
- [Viva Preparation & FAQs](file:///home/epsilon/clg/Enterprise/docs/learning/viva-preparation.md): Questions and answers for academic examination and technical interviews.

### 7. System Design Diagrams (`docs/diagrams/`)
- [System Architecture](file:///home/epsilon/clg/Enterprise/docs/diagrams/system-architecture.md)
- [Layered Architecture](file:///home/epsilon/clg/Enterprise/docs/diagrams/layered-architecture.md)
- [Component Interactions](file:///home/epsilon/clg/Enterprise/docs/diagrams/component-interactions.md)
- [Entity-Relationship Diagram](file:///home/epsilon/clg/Enterprise/docs/diagrams/entity-relationship.md)
- [Class Diagram](file:///home/epsilon/clg/Enterprise/docs/diagrams/class-diagram.md)
- [Use Case Diagram](file:///home/epsilon/clg/Enterprise/docs/diagrams/use-case-diagram.md)
- [Activity Diagrams](file:///home/epsilon/clg/Enterprise/docs/diagrams/activity-diagrams.md)
- [Sequence Diagrams](file:///home/epsilon/clg/Enterprise/docs/diagrams/sequence-diagrams.md)
- [State Transition Diagrams](file:///home/epsilon/clg/Enterprise/docs/diagrams/state-diagrams.md)
