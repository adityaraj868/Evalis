# UML Class Diagram
## Exam Question Re-evaluation & Review Management System

### 1. Class Diagram Specification

```mermaid
classDiagram
    direction TB

    class User {
        -Long id
        -String name
        -String email
        -String passwordHash
        -Role role
        -boolean active
        -LocalDateTime createdAt
        -LocalDateTime updatedAt
        +getId() Long
        +getName() String
        +getEmail() String
        +getRole() Role
    }

    class Exam {
        -Long id
        -String name
        -String subject
        -ExamStatus status
        -LocalDateTime startDate
        -LocalDateTime endDate
        -LocalDateTime reevaluationStart
        -LocalDateTime reevaluationEnd
        -List~Question~ questions
        +isReevaluationOpen(LocalDateTime now) boolean
    }

    class Question {
        -Long id
        -Exam exam
        -Integer questionNumber
        -String questionText
        -Double maxMarks
    }

    class StudentResult {
        -Long id
        -User student
        -Exam exam
        -Double totalMarks
        -String grade
    }

    class QuestionMark {
        -Long id
        -User student
        -Question question
        -Double marksObtained
        -String remarks
    }

    class RecheckRequest {
        -Long id
        -User student
        -Exam exam
        -Question question
        -String reason
        -RequestStatus status
        -Review review
    }

    class Review {
        -Long id
        -RecheckRequest request
        -User faculty
        -ReviewDecision decision
        -Double revisedMarks
        -String comments
        -LocalDateTime reviewedAt
    }

    class AuditLog {
        -Long id
        -User user
        -String action
        -String resourceType
        -Long resourceId
        -String previousValue
        -String updatedValue
        -String description
        -LocalDateTime timestamp
    }

    class ExamStatus {
        <<enumeration>>
        DRAFT
        PUBLISHED
        RE_EVALUATION_OPEN
        RE_EVALUATION_CLOSED
        ARCHIVED
    }

    class RequestStatus {
        <<enumeration>>
        SUBMITTED
        UNDER_REVIEW
        APPROVED
        REJECTED
    }

    class ReviewDecision {
        <<enumeration>>
        APPROVED
        REJECTED
    }

    class Role {
        <<enumeration>>
        STUDENT
        FACULTY
        ADMIN
    }

    User "1" --> "*" StudentResult : results
    User "1" --> "*" QuestionMark : marks
    User "1" --> "*" RecheckRequest : requests
    User "1" --> "*" Review : facultyReviews
    User "1" --> "*" AuditLog : auditActions

    Exam "1" *-- "*" Question : contains
    Exam "1" --> "*" StudentResult : examResults
    Exam "1" --> "*" RecheckRequest : rechecks

    Question "1" --> "*" QuestionMark : marksAwarded
    Question "1" --> "*" RecheckRequest : disputes

    RecheckRequest "1" <--> "0..1" Review : adjudicatedBy

    Exam --> ExamStatus
    RecheckRequest --> RequestStatus
    Review --> ReviewDecision
    User --> Role
```

---

### 2. Exported Diagram Files
- SVG Vector: [class-diagram.svg](class-diagram.svg)
- PNG Raster: [class-diagram.png](class-diagram.png)
