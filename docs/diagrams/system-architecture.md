# System Architecture Diagram
## Exam Question Re-evaluation & Review Management System

### 1. High-Level Architecture

The system is deployed as a layered, modular monolith running Spring Boot 3 on Java 21 LTS with server-side rendered Thymeleaf templates.

```mermaid
graph TD
    Client["Client Web Browser<br/>(Desktop / Mobile)"]
    
    subgraph PresentationTier ["Presentation Layer"]
        Controllers["Spring MVC Controllers<br/>(Student, Faculty, Admin, Auth)"]
        ExceptionAdvice["Global Exception Handler<br/>(@ControllerAdvice)"]
        Templates["Thymeleaf Views & Layouts<br/>(Bootstrap 5 HTML/CSS)"]
    end

    subgraph SecurityTier ["Security & Interception"]
        FilterChain["Spring Security Filter Chain<br/>(Authentication, CSRF, URL Rules)"]
        MethodSec["Method Security<br/>(@PreAuthorize & Anti-IDOR)"]
    end

    subgraph BusinessTier ["Business Logic Layer"]
        ExamSvc["ExamService"]
        MarksSvc["MarksService"]
        RecheckSvc["RecheckRequestService"]
        ReviewSvc["ReviewService"]
        AnalyticsSvc["AnalyticsService"]
        AuditSvc["AuditService"]
        UserSvc["UserService"]
    end

    subgraph DataTier ["Data Access Layer"]
        JPARepos["Spring Data JPA Repositories<br/>(Hibernate ORM 6.6)"]
    end

    subgraph PersistenceTier ["Database Layer"]
        RelationalDB["Relational Database<br/>(H2 / MySQL 8.0)"]
    end

    Client -->|HTTP / HTTPS| FilterChain
    FilterChain --> Controllers
    Controllers --> MethodSec
    MethodSec --> BusinessTier
    BusinessTier --> JPARepos
    JPARepos -->|JDBC / HikariCP| RelationalDB
    Controllers --> Templates
    ExceptionAdvice --> Templates
```

---

### 2. Exported Diagram Files
- SVG Vector: [system-architecture.svg](system-architecture.svg)
- PNG Raster: [system-architecture.png](system-architecture.png)
