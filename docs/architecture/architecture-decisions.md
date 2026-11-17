# Architectural Decision Records (ADR)
## Exam Question Re-evaluation & Review Management System

This document captures the key architectural and design decisions made throughout the evolution of the platform.

---

### ADR-001: Modular Monolithic Architecture over Microservices
- **Status**: Accepted
- **Context**: The system manages university examination re-evaluation, serving students, faculty, and administrators within a single institutional domain.
- **Decision**: Adopt a layered modular monolith built with Spring Boot instead of microservices.
- **Rationale**:
  - Eliminates network serialization latency, distributed transactions (two-phase commit/sagas), and complex service mesh overhead.
  - Ensures ACID transactional guarantees across score updates, review recordings, and audit logging.
  - Keeps operational and deployment overhead minimal while maintaining strict logical boundaries inside services and packages.

---

### ADR-002: Server-Side Rendering with Thymeleaf and Bootstrap 5
- **Status**: Accepted
- **Context**: Need a responsive, accessible, and fast web interface with minimal deployment footprint.
- **Decision**: Use Thymeleaf server-side templating combined with Bootstrap 5 and semantic HTML.
- **Rationale**:
  - Avoids maintaining separate frontend build pipelines (Node, Webpack, React/Angular) and separate API gateways.
  - Eliminates CORS issues, JWT token renewal flows, and client-side state synchronization bugs.
  - Renders complete HTML pages securely on the server with automated CSRF protection and role-based fragment display.

---

### ADR-003: Database-Level Composite Unique Constraint for Re-evaluation Requests
- **Status**: Accepted
- **Context**: In concurrent environments, a student double-clicking or scripting submissions could submit multiple re-evaluation requests for the exact same question.
- **Decision**: Place a composite unique constraint `UNIQUE(student_id, exam_id, question_id)` in the relational database schema in addition to application-level checks.
- **Rationale**:
  - Application-level `existsBy...` queries are subject to Time-of-Check to Time-of-Use (TOCTOU) race conditions in multi-threaded application servers.
  - The database constraint guarantees mathematical uniqueness at the engine level.
  - Spring's `DataIntegrityViolationException` is caught and translated cleanly into a domain `DuplicateRequestException`.

---

### ADR-004: Centralized Immutable Audit Trail
- **Status**: Accepted
- **Context**: Post-examination grade changes require full institutional transparency and defense against grade tampering or disputes.
- **Decision**: Implement an append-only `AuditLog` entity with indexed actor, action, resource, timestamp, and state differentials (`previousValue`, `updatedValue`).
- **Rationale**:
  - Provides a single point of truth for accreditation and grievance auditing.
  - Any review decision or mark adjustment records both old and new scores with faculty remarks.
  - Indexed columns ensure fast administrative search without scanning large tables.

---

### ADR-005: Two-Tier Authorization with Anti-IDOR Protections
- **Status**: Accepted
- **Context**: Standard URL role checks prevent a student from accessing faculty routes, but do not prevent a student from viewing or altering another student's marks or requests.
- **Decision**: Enforce Spring Security filter checks at the perimeter, supplemented by explicit ownership checks in controller and service layers (`userService.getRequiredCurrentUser()`).
- **Rationale**:
  - Completely blocks Horizontal Privilege Escalation (Insecure Direct Object References).
  - Centralized `@ControllerAdvice` maps unauthorized ownership mismatches to HTTP 403 Forbidden with custom error views.
