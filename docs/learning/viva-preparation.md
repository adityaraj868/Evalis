# Viva & Technical Interview Preparation Guide
## Frequently Asked Questions & Model Answers

### Question 1: What is the core problem your system solves?
**Answer**: Traditional academic re-evaluations require re-evaluating the entire paper manually, creating immense overhead for faculty and lack of transparency for students. Our system provides a **granular, question-level re-evaluation platform** where students dispute only specific questions with clear justifications, while faculty can review and revise individual scores with complete audit tracking and question dispute analytics.

---

### Question 2: Why did you choose a monolithic architecture instead of microservices?
**Answer**: For an educational examination platform, data consistency and atomic transactions are paramount. Updating marks and recalculating totals requires ACID transactions. A modular monolith provides strict logical boundaries without the distributed transaction complexity, network latency, and operational overhead of microservices.

---

### Question 3: How do you prevent students from submitting multiple re-evaluation requests for the same question?
**Answer**: We employ a two-layer defense:
1. **Application Layer**: `RecheckRequestService` checks `recheckRequestRepository.existsByStudentAndExamAndQuestion(...)`.
2. **Database Layer**: We enforce a composite unique constraint: `UNIQUE(student_id, exam_id, question_id)`.
Even in concurrent race conditions (e.g. double clicking submit), the database rejects duplicates by throwing a `DataIntegrityViolationException`, which our service maps cleanly to a custom `DuplicateRequestException`.

---

### Question 4: How is Insecure Direct Object Reference (IDOR) prevented?
**Answer**: While Spring Security checks URL-level permissions (e.g. ensuring only users with `ROLE_STUDENT` can access `/student/**`), our controllers implement explicit ownership checks. For any request by ID, the system fetches the authenticated user via `SecurityContextHolder` and asserts that `request.getStudent().getId().equals(currentUser.getId())`. Any violation throws an `UnauthorizedAccessException`, which the `@ControllerAdvice` handler translates to an HTTP 403 Forbidden response.

---

### Question 5: How does the system handle question dispute analytics?
**Answer**: Our `AnalyticsService` computes question dispute frequency by executing a single optimized JPQL aggregation query: `countRequestsByQuestionForExam(examId)`. It compares dispute counts against total student enrollment to determine dispute percentages. If a question's dispute rate exceeds a configurable threshold (e.g., 15%), it is flagged for faculty inspection to identify ambiguous questions or marking discrepancies. It also includes zero-division protection when cohorts have 0 submissions.

---

### Question 6: What happens when a faculty approves a review?
**Answer**: The entire operation executes within a `@Transactional` boundary in `ReviewService`:
1. Validates that the review has not already been decided (decision immutability).
2. Validates the revised marks against the question's `maxMarks` ($0.0 \le \text{revisedMarks} \le \text{maxMarks}$).
3. Updates `QuestionMark.marksObtained`.
4. Triggers atomic recalculation of the student's `StudentResult.totalMarks`.
5. Records the `Review` decision and comments.
6. Transitions the `RecheckRequest` status to `APPROVED`.
7. Emits an immutable structured audit log containing old and new scores.
If any step fails, the entire transaction automatically rolls back.

---

### Question 7: Why did you choose Thymeleaf over React/Vue?
**Answer**: Thymeleaf provides server-side rendering with native Spring Security integration. It eliminates client-side state synchronization bugs, simplifies CSRF token management, and reduces build tool complexity (no Node.js/npm dependencies required), allowing the system to run as a single lightweight JAR file.

---

### Question 8: How does Spring Boot's `@Transactional` annotation work under the hood?
**Answer**: Spring uses **Aspect-Oriented Programming (AOP)** to create a dynamic proxy around `@Transactional` beans. When a method is called:
1. The proxy intercepts the call and starts a database transaction via the `PlatformTransactionManager` (`JpaTransactionManager`).
2. The target business method executes.
3. If the method completes successfully, the proxy commits the transaction.
4. If an unchecked exception (`RuntimeException` or `Error`) is thrown, the proxy automatically issues a rollback command to the database.

---

### Question 9: What is the $N+1$ query problem in Hibernate, and how did you prevent it?
**Answer**: The $N+1$ problem occurs when an application loads $N$ records (e.g. 50 audit logs) and then executes 50 separate SQL queries to fetch each associated child entity (e.g. `log.getUser()`). In this project:
- In `AuditLogRepository`, we used `@EntityGraph(attributePaths = {"user"})` which forces Hibernate to fetch the parent audit log and associated user using a single SQL `LEFT JOIN`.
- We set `spring.jpa.open-in-view: false` to avoid lazy loading queries executing outside transaction boundaries.

---

### Question 10: What are the examination and re-evaluation state lifecycles?
**Answer**:
- **Examination Lifecycle**:
  `DRAFT` (questions editable) &rarr; `PUBLISHED` (questions locked/immutable) &rarr; `RE_EVALUATION_OPEN` (active window, accepts student requests) &rarr; `RE_EVALUATION_CLOSED` (window shut, faculty review ongoing) &rarr; `ARCHIVED` (read-only historical storage).
- **Re-evaluation Request Lifecycle**:
  `SUBMITTED` &rarr; `UNDER_REVIEW` (triggered automatically when faculty opens review details) &rarr; `APPROVED` or `REJECTED` (final, immutable adjudication).

---

### Question 11: Why is storing `total_marks` in `StudentResult` not a violation of 3NF?
**Answer**: While calculating `total_marks` dynamically via `SUM()` is strictly 3NF, querying the sum across all questions for every student on dashboard views creates heavy database read contention. Storing `total_marks` is a **controlled denormalization optimization**:
- It guarantees $O(1)$ read performance for student and faculty overviews.
- Data integrity is preserved by strictly modifying it inside atomic `@Transactional` services (`MarksService`) whenever marks are entered or revised.

---

### Question 12: How is password security implemented?
**Answer**: We use Spring Security's `BCryptPasswordEncoder`:
- Passwords are salted with a 16-byte random salt generated internally by BCrypt and hashed over 10 rounds (`strength = 10`).
- The salt is embedded into the resulting modular crypt format string (e.g., `$2a$10$...`), preventing rainbow table and dictionary attacks.
- Passwords are never logged or returned in plain text.

---

### Question 13: How does your UI design reflect modern enterprise web engineering?
**Answer**: In Phase 10, we implemented a hybrid design system combining **Bunpro** and **Neon Database**:
- **Bunpro Influence**: Structured Bento-grid layout, high-contrast dark mode canvas, and crisp semantic pill badges with status indicator dots.
- **Neon Database Influence**: Razor-sharp `1px` hairline borders, `#00E599` phosphor-emerald accents, a subtle `24px` dot-matrix background, and `JetBrains Mono` telemetry formatting for marks, timestamps, and request IDs.
- **Ambient ASCII Art Background**: A non-intrusive, low-overhead HTML5 canvas (`ascii-bg.js`) that renders architectural waveforms and micro-reactions to cursor movement without compromising WCAG AAA text contrast.

---

### Question 14: What automated test suites exist and what do they verify?
**Answer**: The project contains **67 automated tests** across **11 test classes**:
1. `SecurityAccessTests`: Role-based route access, unauthenticated redirects, and anti-IDOR tests.
2. `ExamLifecycleTests`: State machine transitions, question immutability, date boundary validation.
3. `MarksManagementTests`: Bounds checking ($0 \le \text{mark} \le \text{maxMarks}$), batch persistence, and total marks recalculation.
4. `RecheckRequestCoreTests`: Request window verification, duplicate constraint enforcement, and reason validation.
5. `RequestTrackingTests`: Status progression to `UNDER_REVIEW` and student data isolation.
6. `FacultyReviewWorkflowTests`: Adjudication immutability, score synchronization, rejection handling.
7. `QuestionAnalyticsTests`: Dispute rate calculations, threshold alerts, zero-division safety.
8. `AuditTrailTests`: Structured audit logging, multi-criteria filtering, `@EntityGraph` query verification.
9. `DomainRepositoryTests`: JPA cascading, unique constraints, and custom queries.
10. `HomeControllerSmokeTest` & `ExamReviewApplicationTests`: Context boot and public route rendering.

---

### Question 15: How would you scale this platform to 100,000 students?
**Answer**:
1. **Read Replicas**: Direct dashboard read queries to MySQL read replicas using Spring's `AbstractRoutingDataSource`.
2. **Caching**: Cache immutable published exams and question catalogs using Redis (`@Cacheable`).
3. **Connection Pooling**: Tune HikariCP pool sizes and ensure short transaction lifetimes.
4. **Asynchronous Audit Logging**: Offload `AuditService` event writing using Spring's `@Async` or an event broker like Apache Kafka / RabbitMQ.
5. **Horizontal Scaling**: Because the application is stateless (session management can be backed by Spring Session with Redis), multiple instances can run behind a load balancer like NGINX or AWS ALB.
