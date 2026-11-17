# Backend Request Lifecycle
## Step-by-Step Flow of an HTTP Request

Understanding how an HTTP request travels through the Spring Boot application stack is essential for debugging, performance analysis, and architectural comprehension.

---

### Complete Request Lifecycle Walkthrough

Consider a student submitting a re-evaluation request by sending an HTTP POST to `/student/requests`:

```
   [1] Web Browser (HTTP POST /student/requests)
                 |
                 v
   [2] Embedded Tomcat Web Server (Accepts TCP socket connection)
                 |
                 v
   [3] Spring Security Filter Chain
       - CsrfFilter (Validates CSRF token)
       - SecurityContextHolderFilter (Loads Authentication session)
       - AuthorizationFilter (Checks ROLE_STUDENT authority)
                 |
                 v
   [4] Spring MVC DispatcherServlet (Front Controller)
                 |
                 v
   [5] HandlerMapping (Resolves to StudentController.submitRequest)
                 |
                 v
   [6] HandlerAdapter & DataBinder (Binds form parameters to RecheckRequestFormDto)
                 |
                 v
   [7] StudentController.submitRequest(...)
       - Retrieves current user from UserService.getRequiredCurrentUser()
                 |
                 v
   [8] RecheckRequestService.submitRequest(...) [@Transactional boundary]
       - Exam validation (status, date window)
       - Question validation (ownership, max marks)
       - Marks verification (student has score recorded)
       - Uniqueness check (student, exam, question)
                 |
                 v
   [9] Spring Data JPA Repositories (RecheckRequestRepository, AuditLogRepository)
                 |
                 v
   [10] Hibernate ORM Session (Translates entities to SQL statements)
                 |
                 v
   [11] HikariCP Connection Pool & JDBC Driver
                 |
                 v
   [12] Relational Database Engine (Executes INSERT; enforces constraints)
                 |
                 v
   [13] Transaction Commit (Hibernate flushes changes; connection returned to pool)
                 |
                 v
   [14] Controller completes -> Returns redirect directive "redirect:/student/dashboard"
                 |
                 v
   [15] DispatcherServlet sends HTTP 302 Redirect to Client Browser
```

---

### Error Interception by `GlobalExceptionHandler`
If any step throws an unhandled domain exception:
1. `ResourceNotFoundException`: The exception bubbles out of the service layer.
2. `DispatcherServlet` catches the exception and delegates to `@ControllerAdvice GlobalExceptionHandler`.
3. The advice method matches the exception type, logs the incident, and sets the HTTP response status to 404.
4. It resolves the template `error/404.html` and renders a clean, user-friendly error page without exposing raw stack traces.
