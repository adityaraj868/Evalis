# Component Interactions Diagram
## Exam Question Re-evaluation & Review Management System

### 1. Component Interaction Topology

```mermaid
graph LR
    subgraph Web ["Controllers"]
        SC[StudentController]
        FC[FacultyController]
        AC[AdminController]
    end

    subgraph CoreServices ["Core Services"]
        US[UserService]
        ES[ExamService]
        MS[MarksService]
        RS[RecheckRequestService]
        RVS[ReviewService]
        AS[AnalyticsService]
        ADS[AuditService]
    end

    subgraph Repos ["Repositories"]
        UR[UserRepository]
        ER[ExamRepository]
        QR[QuestionRepository]
        SRR[StudentResultRepository]
        QMR[QuestionMarkRepository]
        RRR[RecheckRequestRepository]
        RVR[ReviewRepository]
        ALR[AuditLogRepository]
    end

    SC --> US
    SC --> ES
    SC --> MS
    SC --> RS

    FC --> US
    FC --> ES
    FC --> MS
    FC --> RS
    FC --> RVS
    FC --> AS

    AC --> US
    AC --> ADS

    US --> UR
    ES --> ER
    ES --> QR
    MS --> QMR
    MS --> SRR
    RS --> RRR
    RVS --> RVR
    RVS --> MS
    AS --> RRR
    AS --> ER
    ADS --> ALR
```

---

### 2. Exported Diagram Files
- SVG Vector: [system-architecture.svg](system-architecture.svg)
