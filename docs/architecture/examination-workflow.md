# Examination Workflow & Lifecycle Management
## Exam Question Re-evaluation & Review Management System

### 1. Examination Lifecycle State Machine
The lifecycle of an examination is strictly controlled by `ExamStatus` enum transitions in `ExamService`.

```mermaid
stateDiagram-v2
    [*] --> DRAFT : Faculty Creates Exam
    DRAFT --> PUBLISHED : Faculty Publishes Exam (Requires >= 1 Question)
    PUBLISHED --> RE_EVALUATION_OPEN : Window Starts / Faculty Opens Window
    RE_EVALUATION_OPEN --> RE_EVALUATION_CLOSED : Window Expires / Faculty Closes Window
    RE_EVALUATION_CLOSED --> ARCHIVED : Faculty Archives Exam
    ARCHIVED --> [*]

    note right of DRAFT
        Editing exam details and adding/removing
        questions is permitted ONLY in DRAFT status.
    end note

    note right of PUBLISHED
        Questions and max marks become frozen.
        Marks entry for students begins.
    end note

    note right of RE_EVALUATION_OPEN
        Students can submit re-evaluation requests
        if reevaluationStart <= now <= reevaluationEnd.
    end note
```

---

### 2. Transition Rules and Constraints

| Source Status | Target Status | Pre-conditions & Validation Rules | Action Performed |
|---|---|---|---|
| *Initial* | `DRAFT` | Title $\ge 3$ characters, Subject valid, Start Date before End Date | Creates new Exam entity |
| `DRAFT` | `DRAFT` | Modifying title, dates, or adding questions | Allowed only in `DRAFT` |
| `DRAFT` | `PUBLISHED` | Must have at least 1 configured Question with $maxMarks > 0$ | Freezes questions, opens exam for grading |
| `PUBLISHED` | `RE_EVALUATION_OPEN` | Re-evaluation start date $\le$ current time $\le$ end date | Allows students to submit recheck requests |
| `RE_EVALUATION_OPEN` | `RE_EVALUATION_CLOSED` | Re-evaluation deadline reached or manual closure | Blocks any new re-evaluation submissions |
| `RE_EVALUATION_CLOSED` | `ARCHIVED` | All pending reviews addressed | Closes exam from active dashboards |

---

### 3. Immutability Enforcement
Once an exam moves from `DRAFT` to `PUBLISHED`:
- Any call to `ExamService.addQuestionToExam()` throws `InvalidStateTransitionException`.
- Any call to `ExamService.updateExam()` attempting to modify questions throws `InvalidStateTransitionException`.
- This ensures historical integrity: student marks and dispute analytics are never invalidated by post-facto question deletions or score weight alterations.
