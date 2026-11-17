# Authorization Flow & Access Control
## Exam Question Re-evaluation & Review Management System

### 1. Multi-Tier Authorization Model
The system enforces authorization at two independent boundaries:
1. **Perimeter / URL-Level Authorization**: Configured in `SecurityConfig.java` using Spring Security's `authorizeHttpRequests`.
2. **Method & Resource Ownership Authorization**: Implemented defensively in controllers and services to prevent Insecure Direct Object References (IDOR) and Horizontal Privilege Escalation.

---

### 2. URL-Level Authorization Matrix

| URL Pattern | Permitted Roles | Failure Action |
|---|---|---|
| `/` | Anonymous / All | Allow |
| `/login` | Anonymous / All | Allow |
| `/css/**`, `/js/**`, `/images/**` | Anonymous / All | Allow |
| `/error`, `/400`, `/403`, `/404` | Anonymous / All | Allow |
| `/student/**` | `ROLE_STUDENT` | HTTP 403 Forbidden / Redirect to Login |
| `/faculty/**` | `ROLE_FACULTY` | HTTP 403 Forbidden / Redirect to Login |
| `/admin/**` | `ROLE_ADMIN` | HTTP 403 Forbidden / Redirect to Login |

---

### 3. Resource-Level Ownership Validation (Anti-IDOR)

Perimeter checks verify that a caller is *a* student, but cannot verify whether they are *the specific* student who owns the requested marksheet or re-evaluation request. To prevent IDOR:

```
[Incoming Request: GET /student/requests/42]
                   |
                   v
[SecurityFilterChain: Caller has ROLE_STUDENT?] ----(No)----> [403 Forbidden]
                   |
                  (Yes)
                   v
[StudentController.trackRequest(42)]
                   |
                   v
[UserService.getRequiredCurrentUser()] ---> Current User (ID: 101)
                   |
                   v
[RecheckRequestService.getRequestById(42)] -> Request Entity (Owner: ID 202)
                   |
                   v
[Ownership Assertion: request.student.id == currentUser.id]
                   |
       +-----------+-----------+
       |                       |
     (Match)               (Mismatch)
       |                       |
       v                       v
[Render View]      [throw UnauthorizedAccessException]
                               |
                               v
                   [GlobalExceptionHandler]
                               |
                               v
                     [HTTP 403 / error/403.html]
```

### 4. Implementation Details in Code

In `StudentController.java`:
```java
User student = userService.getRequiredCurrentUser();
RecheckRequest request = recheckRequestService.getRequestById(id);
if (!request.getStudent().getId().equals(student.getId())) {
    throw new UnauthorizedAccessException("You are not authorized to view another student's re-evaluation request.");
}
```

In `GlobalExceptionHandler.java`:
```java
@ExceptionHandler({UnauthorizedAccessException.class, AccessDeniedException.class})
@ResponseStatus(HttpStatus.FORBIDDEN)
public String handleAccessDenied(Exception ex, Model model) {
    model.addAttribute("error", ex.getMessage());
    return "error/403";
}
```
This architecture ensures that unauthorized queries are stopped cleanly, logged to security warning streams, and presented as informative branded error pages without exposing system stack traces.
