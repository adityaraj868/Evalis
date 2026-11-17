# Layered Architecture
## Exam Question Re-evaluation & Review Management System

### 1. Architectural Philosophy
The application strictly implements a **Layered Architecture** (Presentation, Business Logic, Data Access, and Persistence) following **SOLID principles**, high cohesion, and low coupling. Every tier possesses clear, non-overlapping responsibilities.

```
+-------------------------------------------------------------------------+
|                          Presentation Layer                             |
|  - Controllers: AuthController, StudentController, FacultyController,   |
|                 AdminController                                         |
|  - Exception Handler: GlobalExceptionHandler                            |
|  - Views: Thymeleaf HTML templates, Layout fragments                    |
|  - Form DTOs: ExamFormDto, MarksEntryDto, RecheckRequestFormDto, etc.   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         Business Logic Layer                            |
|  - Services: UserService, ExamService, MarksService,                    |
|              RecheckRequestService, ReviewService, AnalyticsService,     |
|              AuditService                                               |
|  - Validation: State transitions, date ranges, score limits, ownership |
|  - Transactions: Declarative @Transactional boundaries                  |
|  - Exceptions: Domain-specific exceptions                               |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                          Data Access Layer                              |
|  - Repositories: Spring Data JPA Repository Interfaces                  |
|  - Query Methods: JPQL, Derived queries, @EntityGraph optimizations     |
|  - Persistence Unit: Hibernate ORM 6                                    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                           Database Layer                                |
|  - Relational Schema: 8 tables, foreign keys, unique constraints        |
|  - Dialect: H2 (Testing), MySQL 8.0 (Production)                        |
+-------------------------------------------------------------------------+
```

---

### 2. Tier Details & Responsibilities

#### 2.1 Presentation Layer
- **Controllers** receive incoming HTTP requests, unpack parameters or DTOs, invoke business services, handle validation errors, and bind results into the Thymeleaf `Model` or return redirect directives.
- **DTOs (Data Transfer Objects)** decouple presentation inputs from underlying database entities. Examples: `MarksEntryDto` captures batch mark updates, while `RecheckRequestFormDto` isolates submission inputs.
- **Global Exception Handler (`@ControllerAdvice`)** intercepts domain exceptions across all controllers and maps them to HTTP status codes (400 Bad Request, 403 Forbidden, 404 Not Found) with user-friendly error views.

#### 2.2 Business Logic Layer
- **Services** encapsulate the core rules of academic examination and re-evaluation.
- Enforces state machines (e.g., `ExamStatus` transitions, `RequestStatus` transitions).
- Performs defensive assertions (verifying resource ownership to prevent horizontal privilege escalation).
- Manages transactional integrity: methods mutating state (such as approving a review and recalculating total student marks) are marked `@Transactional` so any partial failure triggers an automatic rollback.
- Emits structured audit logs via `AuditService`.

#### 2.3 Data Access Layer
- Leverages **Spring Data JPA** interfaces extending `JpaRepository`.
- Uses JPQL with `@EntityGraph` annotations to avoid $N+1$ query problems when fetching related entities (e.g., `AuditLog` with `User`, `RecheckRequest` with `Student`, `Exam`, and `Question`).
- Provides custom aggregation queries, such as `countRequestsByQuestionForExam` in `RecheckRequestRepository`.

#### 2.4 Database Layer
- Enforces strict referential integrity via Foreign Keys with `ON DELETE CASCADE` or `RESTRICT` where appropriate.
- Guarantees data correctness using Database-level Unique Constraints (e.g., `UNIQUE(student_id, exam_id, question_id)`).

---

### 3. Benefits of this Architecture
1. **Separation of Concerns**: UI changes never impact calculation logic or database tables.
2. **Testability**: Services can be unit-tested in isolation using mock repositories, while controllers can be tested with MockMvc.
3. **Transaction Safety**: Business workflows execute inside clear database transactions, preventing partial updates or orphan records.
4. **Maintainability**: New features (such as notifications or export tools) can plug directly into the service layer without rewriting existing endpoints.
