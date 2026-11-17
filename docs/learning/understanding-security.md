# Understanding Security in Spring Boot 3
## Defense-in-Depth Security Architecture

### 1. The Defense-in-Depth Strategy
Security is implemented across multiple layers rather than relying on a single checkpoint:

```
[ Layer 1: Transport Security ]       HTTPS / TLS encryption in transit
                |
[ Layer 2: Perimeter Security ]       Spring Security FilterChain (URL pattern matching)
                |
[ Layer 3: CSRF Protection ]          Synchronizer Token Pattern on state-changing POST requests
                |
[ Layer 4: Session Security ]         HTTP-Only cookies, session fixation mitigation
                |
[ Layer 5: Method Security ]          @PreAuthorize annotations on services
                |
[ Layer 6: Object-Level Security ]    Anti-IDOR checks verifying resource ownership in controllers
                |
[ Layer 7: Database Constraints ]     Unique constraints preventing unauthorized duplication
```

---

### 2. Common Security Pitfalls Prevented

#### 2.1 Insecure Direct Object References (IDOR)
- **The Threat**: Student 101 logs in, sees their request at `/student/requests/10`, and changes the URL to `/student/requests/11` to view or tamper with another student's submission.
- **The Defense**: `StudentController` calls `userService.getRequiredCurrentUser()` and verifies `request.getStudent().getId().equals(currentUser.getId())`. A mismatch throws `UnauthorizedAccessException`, which renders a 403 Forbidden page and logs the incident.

#### 2.2 Cross-Site Request Forgery (CSRF)
- **The Threat**: A malicious website tricks an authenticated faculty member's browser into submitting a fraudulent review approval request.
- **The Defense**: Spring Security enables CSRF tokens by default. Thymeleaf forms automatically include hidden `_csrf` input tokens. Requests without a valid token are rejected immediately at the filter level.

#### 2.3 Password Security
- Passwords are never stored in plain text.
- Spring Security's `BCryptPasswordEncoder` uses a cryptographic salt and slow hashing algorithm, making dictionary and rainbow table attacks computationally infeasible.
