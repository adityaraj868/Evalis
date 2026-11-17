# Database Relationships & Multiplicities
## Exam Question Re-evaluation & Review Management System

### 1. Entity Multiplicity Matrix

| Primary Entity | Related Entity | Relationship Type | JPA Mapping | Delete Cascade Behavior | Description |
|---|---|---|---|---|---|
| `User` (Student) | `StudentResult` | One-to-Many | `@OneToMany` | CASCADE | A student has multiple overall exam result records. |
| `User` (Student) | `QuestionMark` | One-to-Many | `@OneToMany` | CASCADE | A student has individual marks recorded across questions. |
| `User` (Student) | `RecheckRequest` | One-to-Many | `@OneToMany` | CASCADE | A student can submit multiple question recheck requests. |
| `User` (Faculty) | `Review` | One-to-Many | `@OneToMany` | RESTRICT / CASCADE | Faculty reviews and adjudicates multiple requests. |
| `User` | `AuditLog` | One-to-Many | `@OneToMany` | SET NULL | Actions performed by users are logged in audit history. |
| `Exam` | `Question` | One-to-Many | `@OneToMany` | CASCADE | An exam contains multiple questions numbered sequentially. |
| `Exam` | `StudentResult` | One-to-Many | `@OneToMany` | CASCADE | An exam has scores for all enrolled students. |
| `Exam` | `RecheckRequest` | One-to-Many | `@OneToMany` | CASCADE | Recheck requests are categorized under specific exams. |
| `Question` | `QuestionMark` | One-to-Many | `@OneToMany` | CASCADE | A question has marks awarded to each student. |
| `Question` | `RecheckRequest` | One-to-Many | `@OneToMany` | CASCADE | Multiple students can dispute the same question. |
| `RecheckRequest` | `Review` | One-to-One | `@OneToOne` | CASCADE | A recheck request receives exactly one final faculty review. |

---

### 2. JPA Mapping Details & Bidirectionality

1. **`Exam` <-> `Question`**:
   - `Exam` is the parent aggregate root.
   - `Question` declares `@ManyToOne(fetch = FetchType.LAZY) @JoinColumn(name = "exam_id")`.
   - Marked `FetchType.LAZY` to prevent loading full question graphs unnecessarily when listing exams.

2. **`RecheckRequest` <-> `Review`**:
   - Mapped as a bidirectional `@OneToOne` with `Review` owning the foreign key `request_id`.
   - `Review` enforces `@JoinColumn(name = "request_id", unique = true, nullable = false)`.
   - This architectural decision guarantees that a recheck request can never have more than one adjudication record.

3. **`AuditLog` <-> `User`**:
   - Declares `@ManyToOne(fetch = FetchType.LAZY) @JoinColumn(name = "user_id", nullable = true)`.
   - Allowing `nullable = true` permits logging system-triggered events (such as automated window closures) that lack an interactive human actor.
   - Optimizations use `@EntityGraph(attributePaths = {"user"})` when loading audit logs for administrative presentation to prevent $N+1$ database roundtrips.
