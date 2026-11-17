# UML Use Case Diagram
## Exam Question Re-evaluation & Review Management System

### 1. Use Case Diagram Specification

```mermaid
graph LR
    Student((Student))
    Faculty((Faculty))
    Admin((Administrator))

    subgraph AuthenticationBoundary ["Authentication & Account"]
        UC_Login["Log in with Email & Password"]
        UC_Logout["Log out of Session"]
    end

    subgraph StudentBoundary ["Student Portal"]
        UC_ViewResults["View Exam Results & Breakdown"]
        UC_SubmitReeval["Submit Question Re-evaluation"]
        UC_TrackStatus["Track Request Status"]
    end

    subgraph FacultyBoundary ["Faculty Portal"]
        UC_ManageExams["Create & Publish Exams"]
        UC_EnterMarks["Enter / Update Student Marks"]
        UC_ReviewRequests["Review & Adjudicate Requests"]
        UC_ViewAnalytics["View Question Dispute Analytics"]
    end

    subgraph AdminBoundary ["Administrator Portal"]
        UC_AuditLogs["Filter & Inspect Audit Trail"]
        UC_ManageUsers["Inspect Registered Users"]
    end

    Student --> UC_Login
    Student --> UC_Logout
    Student --> UC_ViewResults
    Student --> UC_SubmitReeval
    Student --> UC_TrackStatus

    Faculty --> UC_Login
    Faculty --> UC_Logout
    Faculty --> UC_ManageExams
    Faculty --> UC_EnterMarks
    Faculty --> UC_ReviewRequests
    Faculty --> UC_ViewAnalytics

    Admin --> UC_Login
    Admin --> UC_Logout
    Admin --> UC_AuditLogs
    Admin --> UC_ManageUsers
```

---

### 2. Exported Diagram Files
- SVG Vector: [use-case-diagram.svg](use-case-diagram.svg)
- PNG Raster: [use-case-diagram.png](use-case-diagram.png)
