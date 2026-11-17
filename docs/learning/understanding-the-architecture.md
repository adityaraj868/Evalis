# Understanding the Architecture
## Design Principles & Patterns in the Exam Review Platform

### 1. Key Architectural Principles

#### 1.1 Single Responsibility Principle (SRP)
Every class in the platform focuses on one specific responsibility:
- `ExamService` manages exam lifecycles and question integrity.
- `MarksService` manages student marks and recalculates totals.
- `ReviewService` manages faculty decisions and marks updates.
- `AnalyticsService` computes aggregation metrics and dispute rates.
- `AuditService` records system-wide audit events.

#### 1.2 Open/Closed Principle (OCP)
The system is open for extension without modifying core logic:
- Adding a new notification channel (e.g. Email or SMS alerts upon review approval) can be done by listening to Spring Application Events or calling an injected notification interface without changing `ReviewService`.

#### 1.3 Dependency Inversion Principle (DIP)
High-level services depend on abstractions (Spring Data JPA interfaces like `ExamRepository`, `UserRepository`), not low-level database connection code.

---

### 2. Design Patterns Applied

1. **Front Controller Pattern**: Implemented by Spring's `DispatcherServlet`, which acts as the single entry point for all incoming HTTP requests.
2. **Data Transfer Object (DTO) Pattern**: DTOs like `MarksEntryDto` and `ExamFormDto` isolate web form data from JPA entities, avoiding unintended entity mutations.
3. **Repository Pattern**: `JpaRepository` abstracts SQL query construction behind clean Java domain methods.
4. **Strategy Pattern**: Spring Security's `AuthenticationManager` selects appropriate `AuthenticationProvider` instances dynamically.
5. **Template Method Pattern**: Thymeleaf layouts use header/footer fragments to enforce uniform UI styling across all pages.
