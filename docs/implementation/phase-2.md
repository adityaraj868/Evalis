# Phase 2 — Authentication & Authorization
## Exam Question Re-evaluation & Review Management System

**Phase Status**: `COMPLETED`  
**Execution Date**: November 18, 2026  
**Lead Architect**: Senior Software Architect & Lead Backend Engineer  

---

## 1. Objectives & Requirements

Phase 2 establishes robust, enterprise-grade Role-Based Access Control (RBAC) and backend resource ownership validation for the platform:
- **Roles Required**: `STUDENT`, `FACULTY`, `ADMIN`.
- **Spring Security Integration**: Method security via `@EnableMethodSecurity(prePostEnabled = true)`.
- **Route Protection**: HTTP filter chain restricting `/student/**` to `ROLE_STUDENT`, `/faculty/**` to `ROLE_FACULTY`, and `/admin/**` to `ROLE_ADMIN`.
- **Backend Ownership Validation**: Strict resource isolation preventing horizontal privilege escalation (e.g. students accessing another student's exam breakdown or re-evaluation request details).
- **Error Handling**: Branded 401 Unauthorized, 403 Forbidden, 404 Not Found, and 400 Bad Request error views with centralized `@ControllerAdvice` exception handling.
- **Verification**: Dedicated automated test suite covering all roles, unauthorized cross-access attempts, unauthenticated redirects, and credential validation.

---

## 2. Architectural Design & Implementation

### 2.1 Security Configuration (`SecurityConfig.java`)
- Enabled method security: `@EnableMethodSecurity(prePostEnabled = true)` allows fine-grained declarative authorization on services and controller methods.
- Refined URL security rules:
  - Public routes: `/`, `/css/**`, `/js/**`, `/images/**`, `/login`, `/403`, `/404`, `/400`, `/error`, `/h2-console/**`.
  - Student routes: `/student/**` requires `ROLE_STUDENT`.
  - Faculty routes: `/faculty/**` requires `ROLE_FACULTY`.
  - Administrator routes: `/admin/**` requires `ROLE_ADMIN`.
- Form Login: Configured with `RoleBasedAuthenticationSuccessHandler` for intelligent post-authentication redirection to `/student/dashboard`, `/faculty/dashboard`, or `/admin/dashboard`.
- Password Hashing: BCrypt password encoder with standard salt rounds.

### 2.2 Domain Exception Hierarchy (`com.example.examreview.exception`)
To decouple HTTP status codes from business logic and avoid leaking raw stack traces, a centralized domain exception hierarchy was introduced:
1. `UnauthorizedAccessException`: Thrown when an authenticated user attempts to access resources outside their ownership (e.g., another student's request) or lacks required permissions.
2. `ResourceNotFoundException`: Thrown when an entity ID (Exam, Question, RecheckRequest) does not exist in the database.
3. `InvalidStateTransitionException`: Thrown when an operation violates domain lifecycle rules (e.g., altering closed exams).
4. `DuplicateRequestException`: Thrown when duplicate submissions occur.
5. `ValidationException`: Thrown for general business constraint violations.

### 2.3 Centralized Exception Handling (`GlobalExceptionHandler.java`)
- Annotates `@ControllerAdvice` to intercept exceptions across all web controllers:
  - `UnauthorizedAccessException` and Spring Security's `AccessDeniedException` → Maps to HTTP 403 and renders `error/403.html`.
  - `ResourceNotFoundException` → Maps to HTTP 404 and renders `error/404.html`.
  - `InvalidStateTransitionException` & `DuplicateRequestException` → Maps to HTTP 400 and renders `error/400.html`.

### 2.4 User Service & Backend Authorization (`UserService.java`)
Added defensive authentication and role assertion utilities:
- `getRequiredCurrentUser()`: Safely retrieves the currently authenticated user entity from `SecurityContextHolder`, throwing `UnauthorizedAccessException` if the session is unauthenticated or invalid.
- `validateRole(User user, Role expectedRole)`: Validates that the active user possesses the expected role, preventing privilege escalation.

### 2.5 Horizontal Privilege Escalation Prevention (`StudentController.java`)
- **Exam Breakdown (`/student/exams/{id}`)**: Ensures that only students who have an official `StudentResult` enrollment record for the examination can view the question-wise marks breakdown.
- **Request Details (`/student/requests/{id}`)**: Validates that `request.getStudent().getId().equals(currentUser.getId())`. Any attempt by another student to view or guess request IDs is blocked with an HTTP 403 `UnauthorizedAccessException`.

---

## 3. Files Created & Modified

| File Path | Action | Description |
|---|---|---|
| `config/SecurityConfig.java` | Modified | Added `@EnableMethodSecurity`, permitted error pages (`/404`, `/400`, `/error`). |
| `service/UserService.java` | Modified | Added `getRequiredCurrentUser()` and role assertion utilities. |
| `controller/StudentController.java` | Modified | Added backend resource ownership checks using `UnauthorizedAccessException`. |
| `controller/FacultyController.java` | Modified | Integrated `ResourceNotFoundException` and `getRequiredCurrentUser()`. |
| `exception/UnauthorizedAccessException.java` | Created | Exception representing forbidden access or IDOR attempts. |
| `exception/ResourceNotFoundException.java` | Created | Exception representing missing entities (404). |
| `exception/InvalidStateTransitionException.java` | Created | Exception for domain lifecycle violations. |
| `exception/DuplicateRequestException.java` | Created | Exception for duplicate request attempts. |
| `exception/ValidationException.java` | Created | Exception for business validation failures. |
| `exception/GlobalExceptionHandler.java` | Created | Centralized `@ControllerAdvice` error translation and view rendering. |
| `templates/error/404.html` | Created | User-friendly branded 404 Not Found page. |
| `templates/error/400.html` | Created | User-friendly branded 400 Bad Request page. |
| `test/.../security/SecurityAccessTests.java` | Created | 8 automated security tests covering RBAC and IDOR prevention. |

---

## 4. Testing & Verification

Executed the automated test suite via Maven Surefire:
- **`SecurityAccessTests`**:
  1. `testPublicRoutesPermitted`: Verified `/`, `/login`, `/403` return 200 OK without authentication.
  2. `testUnauthenticatedRedirectsToLogin`: Verified unauthenticated calls to `/student/**`, `/faculty/**`, `/admin/**` redirect to `/login`.
  3. `testValidLoginRedirects`: Verified student, faculty, and admin users are redirected to their respective dashboards post-login.
  4. `testInvalidLoginFails`: Verified incorrect password causes redirection to `/login?error=true`.
  5. `testStudentRoleRestrictions`: Verified student cannot access faculty or admin endpoints (HTTP 403).
  6. `testFacultyRoleRestrictions`: Verified faculty cannot access student or admin endpoints (HTTP 403).
  7. `testAdminRoleAccess`: Verified admin has full access to admin dashboard, students list, and audit logs.
  8. `testHorizontalPrivilegeEscalationPrevented`: Verified that Student 2 attempting to view Student 1's request via `/student/requests/{id}` is blocked with HTTP 403.

**Full Test Suite**: 20 tests run, 0 failures, 0 errors, 0 skipped.

---

## 5. Exit Criteria Verification

- [x] Each role (`STUDENT`, `FACULTY`, `ADMIN`) can access only its authorized functionality and resources.
- [x] Unauthenticated users are redirected to `/login`.
- [x] Unauthorized access produces clean HTTP 403 responses without stack traces.
- [x] Cross-student resource access (IDOR) is blocked on the backend.
- [x] Automated security test suite is in place and verified.
