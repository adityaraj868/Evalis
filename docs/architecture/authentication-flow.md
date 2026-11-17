# Authentication Flow
## Exam Question Re-evaluation & Review Management System

### 1. Authentication Overview
The application uses **Spring Security 6** with session-based cookie authentication and BCrypt password encryption ($2^{10}$ hashing rounds). Form-based login handles authentication requests at `/login`.

---

### 2. Sequence Diagram: User Authentication

```mermaid
sequenceDiagram
    autonumber
    actor User as User (Browser)
    participant Filter as SecurityFilterChain (UsernamePasswordAuthenticationFilter)
    participant AuthManager as ProviderManager (AuthenticationManager)
    participant Provider as DaoAuthenticationProvider
    participant UserDetailsService as CustomUserDetailsService
    participant UserRepo as UserRepository
    participant SuccessHandler as RoleBasedAuthenticationSuccessHandler
    participant Session as HttpSession / SecurityContext

    User->>Filter: POST /login (username, password)
    Filter->>AuthManager: authenticate(UsernamePasswordAuthenticationToken)
    AuthManager->>Provider: authenticate(token)
    Provider->>UserDetailsService: loadUserByUsername(email)
    UserDetailsService->>UserRepo: findByEmailAndActiveTrue(email)
    UserRepo-->>UserDetailsService: Optional<User>
    UserDetailsService-->>Provider: UserDetails (with ROLE_*)
    Provider->>Provider: passwordEncoder.matches(rawPassword, encodedPassword)
    alt Password Valid
        Provider-->>AuthManager: Fully Authenticated Authentication Token
        AuthManager-->>Filter: Authentication Object
        Filter->>Session: SecurityContextHolder.setContext(auth)
        Filter->>SuccessHandler: onAuthenticationSuccess(request, response, auth)
        alt Role == ROLE_STUDENT
            SuccessHandler-->>User: HTTP 302 Redirect to /student/dashboard
        else Role == ROLE_FACULTY
            SuccessHandler-->>User: HTTP 302 Redirect to /faculty/dashboard
        else Role == ROLE_ADMIN
            SuccessHandler-->>User: HTTP 302 Redirect to /admin/dashboard
        end
    else Invalid Credentials / Inactive User
        Provider-->>Filter: BadCredentialsException / UsernameNotFoundException
        Filter-->>User: HTTP 302 Redirect to /login?error=true
    end
```

---

### 3. Key Components
1. **`CustomUserDetailsService`**:
   - Queries `UserRepository.findByEmailAndActiveTrue(email)`.
   - Maps the database `User` entity to Spring Security's `UserDetails` contract.
   - Prepends `ROLE_` to the database role string (e.g. `ROLE_STUDENT`, `ROLE_FACULTY`, `ROLE_ADMIN`).
   - Ensures inactive accounts cannot authenticate.

2. **`BCryptPasswordEncoder`**:
   - One-way cryptographically secure salted hash generator.
   - Prevents plain-text password leakage.

3. **`RoleBasedAuthenticationSuccessHandler`**:
   - Inspects the authenticated user's granted authorities.
   - Directs students to `/student/dashboard`, faculty to `/faculty/dashboard`, and admins to `/admin/dashboard`.
   - Falls back safely to `/` for unrecognized roles.

4. **Session Management & Logout**:
   - Invalidation of HTTP session on logout.
   - Clear cookies and purge `SecurityContextHolder`.
