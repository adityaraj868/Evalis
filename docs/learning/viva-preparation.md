# Viva & Technical Interview Preparation Guide
## Frequently Asked Questions & Model Answers

### Question 1: What is the core problem your system solves?
**Answer**: Traditional academic re-evaluations require re-evaluating the entire paper manually, creating immense overhead for faculty and lack of transparency for students. Our system provides a **granular, question-level re-evaluation platform** where students dispute only specific questions with clear justifications, while faculty can review and revise individual scores with complete audit tracking and question dispute analytics.

---

### Question 2: Why did you choose a monolithic architecture instead of microservices?
**Answer**: For an educational examination platform, data consistency and atomic transactions are paramount. Updating marks and recalculating totals requires ACID transactions. A modular monolith provides strict logical boundaries without the distributed transaction complexity, network latency, and operational overhead of microservices.

---

### Question 3: How do you prevent students from submitting multiple re-evaluation requests for the same question?
**Answer**: We employ a two-layer defense. First, at the application layer, `RecheckRequestService` checks `recheckRequestRepository.existsByStudentAndExamAndQuestion(...)`. Second, at the database layer, we enforce a composite unique constraint: `UNIQUE(student_id, exam_id, question_id)`. Even in the event of concurrent race conditions, the database rejects duplicates by throwing a `DataIntegrityViolationException`, which our service maps cleanly to a `DuplicateRequestException`.

---

### Question 4: How is Insecure Direct Object Reference (IDOR) prevented?
**Answer**: While Spring Security checks URL-level permissions (e.g. ensuring only users with `ROLE_STUDENT` can access `/student/**`), our controllers implement explicit ownership checks. For any request by ID, the system fetches the authenticated user via `SecurityContextHolder` and asserts that `request.getStudent().getId().equals(currentUser.getId())`. Any violation throws an `UnauthorizedAccessException`, which the `@ControllerAdvice` handler translates to an HTTP 403 Forbidden response.

---

### Question 5: How does the system handle question dispute analytics?
**Answer**: Our `AnalyticsService` computes question dispute frequency by executing a single optimized JPQL aggregation query: `countRequestsByQuestionForExam(examId)`. It compares dispute counts against total student enrollment to determine dispute percentages. If a question's dispute rate exceeds a configurable threshold (e.g., 15%), it is flagged for faculty inspection to identify ambiguous questions or marking discrepancies.

---

### Question 6: What happens when a faculty approves a review?
**Answer**: The entire operation executes within a `@Transactional` boundary in `ReviewService`. The service validates the revised marks against the question's `maxMarks`, updates the `QuestionMark`, calls `MarksService` to recalculate the student's `totalMarks` in `StudentResult`, records the `Review` decision, transitions the `RecheckRequest` status to `APPROVED`, and emits a structured audit log containing old and new scores. If any step fails, the entire transaction rolls back.

---

### Question 7: Why did you choose Thymeleaf over React/Vue?
**Answer**: Thymeleaf provides server-side rendering with native Spring Security integration. It eliminates client-side state synchronization bugs, simplifies CSRF token management, and reduces build tool complexity (no Node.js/npm dependencies required), allowing the system to run as a single lightweight JAR file.
