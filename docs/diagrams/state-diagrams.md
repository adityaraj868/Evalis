# State Diagrams
## Exam Question Re-evaluation & Review Management System

### 1. Examination Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> DRAFT : Faculty Creates Exam
    DRAFT --> PUBLISHED : Faculty Publishes Exam (Requires >= 1 Question)
    PUBLISHED --> RE_EVALUATION_OPEN : Window Opens / Faculty Opens Window
    RE_EVALUATION_OPEN --> RE_EVALUATION_CLOSED : Window Expires / Faculty Closes Window
    RE_EVALUATION_CLOSED --> ARCHIVED : Faculty Archives Exam
    ARCHIVED --> [*]
```

- SVG Vector: [exam-state-diagram.svg](exam-state-diagram.svg)
- PNG Raster: [exam-state-diagram.png](exam-state-diagram.png)

---

### 2. Re-evaluation Request Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> SUBMITTED : Student Submits Request
    SUBMITTED --> UNDER_REVIEW : Faculty Opens Request Details
    UNDER_REVIEW --> APPROVED : Faculty Approves & Updates Marks
    UNDER_REVIEW --> REJECTED : Faculty Rejects with Feedback
    APPROVED --> [*]
    REJECTED --> [*]
```

- SVG Vector: [request-state-diagram.svg](request-state-diagram.svg)
- PNG Raster: [request-state-diagram.png](request-state-diagram.png)
