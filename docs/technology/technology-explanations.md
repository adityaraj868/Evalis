# Technology Explanations & Justification
## Exam Question Re-evaluation & Review Management System

### 1. Java 21 LTS
- **Why Java 21?** Java 21 brings key LTS performance enhancements, virtual threads capability, record patterns, strongly-typed pattern matching in switch expressions, and improved memory efficiency.
- **Application Relevance**: Used across all domain models, services, DTOs, and exception hierarchies for type safety and expressiveness.

---

### 2. Spring Boot 3.4.3
- **Why Spring Boot 3?** Built on Spring Framework 6 and Jakarta EE 10 baseline, offering modern dependency injection, standardized configuration via `application.yml`, integrated testing support, and rapid auto-configuration of datasources and security chains.
- **Application Relevance**: Serves as the central orchestration framework managing component lifecycles, configuration properties, and database connection pools.

---

### 3. Spring Security 6
- **Why Spring Security 6?** Replaces legacy `WebSecurityConfigurerAdapter` with modern, lambda-based `SecurityFilterChain` declarations and `@EnableMethodSecurity`.
- **Application Relevance**:
  - Enforces role separation (`ROLE_STUDENT`, `ROLE_FACULTY`, `ROLE_ADMIN`).
  - Protects routes against unauthenticated or unauthorized access.
  - Automatically injects and validates CSRF tokens across all POST forms.
  - Transparently manages authenticated sessions via `SecurityContextHolder`.

---

### 4. Spring Data JPA & Hibernate 6
- **Why Spring Data JPA?** Eliminates boilerplate DAO code by generating dynamic SQL implementations for repository interfaces at startup.
- **Why Hibernate 6?** Provides an advanced query translator (SQM - Semantic Query Model) generating cleaner, optimized SQL queries and supporting `@EntityGraph` for precise fetch plan control.
- **Application Relevance**: Enables declarative CRUD, relational mapping across the 8 tables, and type-safe JPQL aggregation queries.

---

### 5. Thymeleaf & Thymeleaf Spring Security 6 Dialect
- **Why Thymeleaf?** Unlike legacy JSP or client-heavy single page apps, Thymeleaf is a modern server-side template engine that processes natural HTML templates directly.
- **Application Relevance**:
  - Allows pages to be viewed directly in browsers as static prototypes.
  - Dynamic tags (`th:each`, `th:if`, `th:text`) seamlessly inject model data into HTML.
  - `sec:authorize="hasRole(...)"` allows dynamic rendering of role-appropriate navigation links and action buttons directly within the layout.

---

### 6. HikariCP Connection Pool
- **Why HikariCP?** Default connection pool in Spring Boot, recognized as the fastest, most reliable, and lightweight JDBC connection pool in the Java ecosystem.
- **Application Relevance**: Reuses database connections efficiently across concurrent user sessions, preventing socket exhaustion during peak exam results release periods.
