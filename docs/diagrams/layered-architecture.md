# Layered Architecture Diagram
## Exam Question Re-evaluation & Review Management System

### 1. Layered Architecture

```mermaid
graph TD
    subgraph Presentation ["Presentation Layer"]
        Controllers["Controllers & Exception Advice"]
        Views["Thymeleaf HTML Views (Bootstrap 5)"]
        DTOs["Form Data Transfer Objects (DTOs)"]
    end

    subgraph Security ["Security Layer"]
        Filter["Spring Security Filter Chain"]
        MethodSec["Role-Based Method Security & Anti-IDOR"]
    end

    subgraph Service ["Business Logic Layer"]
        Services["Domain Services (@Transactional)"]
        Exceptions["Domain Specific Exceptions"]
    end

    subgraph Persistence ["Data Access Layer"]
        Repositories["Spring Data JPA Repositories"]
        Entities["Hibernate ORM 6 Entities"]
    end

    subgraph Database ["Relational Database"]
        RDBMS["MySQL 8.0 / H2 Relational Database"]
    end

    Presentation --> Security
    Security --> Service
    Service --> Persistence
    Persistence --> Database
```

---

### 2. Exported Diagram Files
- SVG Vector: [layered-architecture.svg](layered-architecture.svg)
- PNG Raster: [layered-architecture.png](layered-architecture.png)
