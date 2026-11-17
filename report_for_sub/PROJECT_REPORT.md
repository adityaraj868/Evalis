# Exam Question Re-evaluation and Review Management System
## Final Project Report

**Course Code**: UCS553: Enterprise Web Application  
**Institution**: Thapar Institute of Engineering & Technology, Patiala  
**Department**: Computer Science and Engineering Department  
**Project Guide / Supervisor**: Chinu  
**Academic Session**: November 2026  

---

### Team Members
| S. No. | Student Name | Roll Number |
|---|---|---|
| 1 | Adityaraj Singh | 1024170148 |
| 2 | Sparsh Khandelwal | 1024170139 |
| 3 | Vaibhav Goyal | 1024170002 |

---

## 1. Executive Summary & Deliverables
This final project report documents the design, implementation, verification, and deployment of the **Exam Question Re-evaluation and Review Management System**. The deliverables produced include:
1. **Final Word Report**: `Exam_Review_System_Final_Report.docx` (both in `report_for_sub/` and root directory)
2. **Final PDF Report**: `Exam_Review_System_Final_Report.pdf` (23 pages, formatted with high-resolution diagrams and actual screenshots)
3. **UML & Architecture Diagrams**: High-resolution vector SVGs and PNGs in `docs/diagrams/`
4. **Summary Report**: Detailed section-by-section audit of actual screenshots, technical diagrams, and code alignments.

---

## 2. Technical Stack Verification
- **Runtime & Language**: Java 21 (LTS)
- **Framework**: Spring Boot 3.4.3
- **Security**: Spring Security 6 (BCrypt password encoding, role-based HTTP security: `STUDENT`, `FACULTY`, `ADMIN`)
- **Persistence**: Spring Data JPA / Hibernate 6 ORM
- **Database**: MySQL 8.0+ (Driver: `com.mysql.cj.jdbc.Driver`, `open-in-view: false` enforced for transaction safety)
- **Templating**: Thymeleaf 3 with Bootstrap 5.3 & Bootstrap Icons
- **Build Tool**: Apache Maven (Maven Compiler 3.13.0, Source/Target 21)
- **Testing**: JUnit 5 (`org.junit.jupiter`), Mockito 5, AssertJ, Spring Boot Test Starter (100% test pass rate across 10 suites)

---

## 3. Diagrams Generated & Embedded (docs/diagrams/)
1. **Figure 2.1**: Multi-Tier Enterprise System Architecture (`system-architecture.png`)
2. **Figure 2.2**: Layered Software Architecture (`layered-architecture.png`)
3. **Figure 2.3**: UML Use Case Diagram (`use-case-diagram.png`)
4. **Figure 2.4**: UML Class Diagram of Domain Model Entities (`class-diagram.png`)
5. **Figure 2.5**: UML Activity Diagram — Re-evaluation Request and Review Lifecycle (`activity-diagram.png`)
6. **Figure 2.6**: Sequence Diagram — Student Re-evaluation Request Submission (`sequence-diagram-submission.png`)
7. **Figure 2.7**: Sequence Diagram — Faculty Review and Mark Revision Workflow (`sequence-diagram-review.png`)
8. **Figure 2.8**: Examination Lifecycle State Transition Diagram (`exam-state-diagram.png`)
9. **Figure 2.9**: Re-evaluation Request Lifecycle State Transition Diagram (`request-state-diagram.png`)
10. **Figure 2.10**: Entity-Relationship (ER) Schema Diagram (`er-diagram.png`)

---

## 4. Actual Website Screenshots Embedded (docs/website-screenshots/)
1. **Figure 4.1**: Student Portal Dashboard — Overview Cards and Enrolled Examinations Table (`student-dashboard.png`)
2. **Figure 4.2**: Examination Question-Wise Marks Breakdown and Re-evaluation Action Interface (`question_marks.png`)
3. **Figure 4.3**: Question Re-evaluation Request Submission Form with Mandatory Reason Input (`reevaluation-form.png`)
4. **Figure 4.4**: Faculty Portal Dashboard — Examination Overview and Pending Reviews Worklist (`faculty-dashboard.png`)
5. **Figure 4.5**: Question-Wise Dispute Analytics and Request Distribution Heatmap (`question-analytics.png`)
6. **Figure 4.6**: System Compliance Audit Log Interface — Chronological Administrative Action Trail (`audit-logs.png`)
