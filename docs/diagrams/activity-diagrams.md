# Activity Diagrams
## Exam Question Re-evaluation & Review Management System

### 1. Student Re-evaluation Submission Activity Flow

```mermaid
flowchart TD
    Start([Student Starts Submission]) --> LoginCheck{Logged in as Student?}
    LoginCheck -- No --> RedirectLogin[Redirect to Login] --> End([End])
    LoginCheck -- Yes --> SelectExam[Select Published Exam]
    SelectExam --> InspectMarks[View Question-level Marks]
    InspectMarks --> WindowCheck{Re-evaluation Window Active?}
    WindowCheck -- No --> ShowClosed[Display 'Window Closed' Message] --> End
    WindowCheck -- Yes --> OpenForm[Open Re-evaluation Form]
    OpenForm --> FillReason[Enter Disputed Question & Rationale]
    FillReason --> Submit[Click Submit]
    Submit --> ValCheck{Reason >= 5 chars & Not Already Disputed?}
    ValCheck -- No --> ShowError[Display Validation Error] --> FillReason
    ValCheck -- Yes --> SaveDB[(Persist RecheckRequest)]
    SaveDB --> LogAudit[(Record Audit Log: REQUEST_SUBMITTED)]
    LogAudit --> ShowSuccess[Show Success Confirmation Alert] --> End
```

---

### 2. Exported Diagram Files
- SVG Vector: [activity-diagram.svg](activity-diagram.svg)
- PNG Raster: [activity-diagram.png](activity-diagram.png)
