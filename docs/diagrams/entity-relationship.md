# Entity Relationship (ER) Diagram
## Exam Question Re-evaluation & Review Management System

### 1. ER Diagram Specification

```mermaid
erDiagram
    USERS ||--o{ STUDENT_RESULTS : "has results"
    USERS ||--o{ QUESTION_MARKS : "earns marks"
    USERS ||--o{ RECHECK_REQUESTS : "submits"
    USERS ||--o{ REVIEWS : "conducts"
    USERS ||--o{ AUDIT_LOGS : "triggers"

    EXAMS ||--|{ QUESTIONS : "contains"
    EXAMS ||--o{ STUDENT_RESULTS : "records"
    EXAMS ||--o{ RECHECK_REQUESTS : "evaluates"

    QUESTIONS ||--o{ QUESTION_MARKS : "graded on"
    QUESTIONS ||--o{ RECHECK_REQUESTS : "disputed in"

    RECHECK_REQUESTS ||--o| REVIEWS : "adjudicated by"

    USERS {
        bigint id PK
        string name
        string email UK
        string password_hash
        string role
        boolean active
        timestamp created_at
    }

    EXAMS {
        bigint id PK
        string name
        string subject
        string status
        timestamp start_date
        timestamp end_date
        timestamp reevaluation_start
        timestamp reevaluation_end
    }

    QUESTIONS {
        bigint id PK
        bigint exam_id FK
        int question_number
        text question_text
        double max_marks
    }

    STUDENT_RESULTS {
        bigint id PK
        bigint student_id FK
        bigint exam_id FK
        double total_marks
        string grade
    }

    QUESTION_MARKS {
        bigint id PK
        bigint student_id FK
        bigint question_id FK
        double marks_obtained
        string remarks
    }

    RECHECK_REQUESTS {
        bigint id PK
        bigint student_id FK
        bigint exam_id FK
        bigint question_id FK
        text reason
        string status
    }

    REVIEWS {
        bigint id PK
        bigint request_id FK,UK
        bigint faculty_id FK
        string decision
        double revised_marks
        text comments
        timestamp reviewed_at
    }

    AUDIT_LOGS {
        bigint id PK
        bigint user_id FK
        string action
        string resource_type
        bigint resource_id
        text previous_value
        text updated_value
        text description
        timestamp timestamp
    }
```

---

### 2. Exported Diagram Files
- SVG Vector: [er-diagram.svg](er-diagram.svg)
- PNG Raster: [er-diagram.png](er-diagram.png)
