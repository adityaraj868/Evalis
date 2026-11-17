# Technology Stack & Tooling
## Exam Question Re-evaluation & Review Management System

### 1. Technology Matrix

| Layer / Concern | Technology | Version | Purpose |
|---|---|---|---|
| **Runtime Environment** | Java OpenJDK | 21 LTS | Core programming language runtime (Modern switch expressions, pattern matching, records) |
| **Framework** | Spring Boot | 3.4.3 | Application foundation, auto-configuration, dependency injection, and embedded container |
| **Web MVC** | Spring MVC | 6.2.x | Model-View-Controller request routing, binding, and validation |
| **Security** | Spring Security | 6.4.x | Role-based access control, session authentication, BCrypt hashing, method security |
| **Templating Engine** | Thymeleaf | 3.1.x | Server-side HTML rendering, layout dialect, CSRF token injection |
| **Data Persistence** | Spring Data JPA / Hibernate | 6.6.8.Final | Object-Relational Mapping (ORM), declarative repositories, JPQL |
| **Database (Dev/Test)**| H2 Database | 2.3.232 | Fast, zero-config in-memory relational database for testing and quick local run |
| **Database (Prod)** | MySQL Connector/J | 8.x / 9.x | Enterprise relational database for persistent production deployments |
| **Connection Pooling** | HikariCP | 5.1.x | High-performance JDBC connection pool |
| **UI Components** | Bootstrap | 5.3.x | Responsive design, modern card styling, modals, alert banners, and badges |
| **Build Automation** | Apache Maven | 3.9+ | Dependency resolution, compilation, resource filtering, and test execution |
| **Testing Framework** | JUnit Jupiter (JUnit 5) | 5.11.x | Unit and integration test orchestration |
| **Mocking & Web Test** | Mockito & Spring Test (MockMvc) | Standard | Controller testing, security filter chain testing, transaction rollbacks |

---

### 2. Dependency Declarations (`pom.xml` summary)

The project dependencies are strictly managed via Spring Boot starter BOM:
- `spring-boot-starter-web`: Embedded Tomcat, Spring MVC, Jackson JSON.
- `spring-boot-starter-security`: Spring Security Core, Web filter chains.
- `spring-boot-starter-data-jpa`: Hibernate ORM, Spring Data, HikariCP, JPA API.
- `spring-boot-starter-thymeleaf`: Thymeleaf view resolver and dialect support.
- `thymeleaf-extras-springsecurity6`: Thymeleaf tags for conditional rendering based on user roles (`sec:authorize`).
- `com.h2database:h2`: In-memory database scope test and runtime.
- `com.mysql:mysql-connector-j`: MySQL JDBC driver for production environments.
- `spring-boot-starter-test`: JUnit 5, AssertJ, Mockito, Spring Test, Spring Security Test.
