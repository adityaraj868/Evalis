# Testing Strategy & Quality Assurance
## Exam Question Re-evaluation & Review Management System

### 1. Testing Philosophy
The testing strategy adheres to the **Test Pyramid principle**, emphasizing automated regression tests spanning Unit Tests, Data Layer Tests, Service Integration Tests, and Web Security Filter Tests.

```
            / \
           /   \       Web & Security Tests (MockMvc)
          /  8  \      - Role access, redirects, anti-IDOR
         /-------\
        /         \     Service Integration Tests (@SpringBootTest)
       /    50     \    - Exam lifecycle, marks recalculation,
      /             \     recheck core, reviews, analytics, audits
     /---------------\
    /                 \   Repository Layer Unit Tests (@DataJpaTest)
   /         9         \  - Entity relationships, cascades, unique constraints
  /---------------------\
```

---

### 2. Test Execution Profiles & Isolation
- **Active Profile**: `test` (configured in `src/test/resources/application-test.yml`).
- **Database Engine**: H2 in-memory database (`jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=MySQL`).
- **Isolation Principle**:
  - Each integration test class resets database state in a `@BeforeEach` fixture.
  - Foreign key dependency order is strictly respected during cleanup:
    `ReviewRepository` $\rightarrow$ `RecheckRequestRepository` $\rightarrow$ `QuestionMarkRepository` $\rightarrow$ `StudentResultRepository` $\rightarrow$ `QuestionRepository` $\rightarrow$ `ExamRepository` $\rightarrow$ `AuditLogRepository` $\rightarrow$ `UserRepository`.

---

### 3. Coverage Focus Areas
1. **Security & Access Control**:
   - Verification that unauthenticated users are redirected to `/login`.
   - Verification that students cannot access `/faculty/**` or `/admin/**` (returns HTTP 403).
   - Verification that faculty cannot access `/admin/**` (returns HTTP 403).
   - Verification that students cannot access another student's request details (Anti-IDOR).
2. **State Transition Integrity**:
   - Enforcing valid progression of `ExamStatus` and `RequestStatus`.
   - Rejecting invalid transitions (e.g. attempting to review an already-approved request).
3. **Data Integrity & Recalculation**:
   - Verifying that updating question marks automatically recalculates the student's total result.
   - Enforcing bounds on student marks ($0.0 \le \text{mark} \le \text{maxMarks}$).
4. **Race Condition & Duplicate Prevention**:
   - Verifying that duplicate submissions for the same question fail with `DuplicateRequestException`.
5. **Analytics & Aggregations**:
   - Testing dispute percentage computations and threshold alerts with zero-division safety.
6. **Audit Trail Completeness**:
   - Ensuring structured logs are emitted on submissions, reviews, and marks updates.
