# Phase 9 — Centralized Audit Trail
## Exam Question Re-evaluation & Review Management System

**Phase Status**: `COMPLETED`  
**Execution Date**: November 18, 2026  
**Lead Architect**: Senior Software Architect & Lead Backend Engineer  

---

## 1. Objectives & Requirements

Phase 9 establishes an enterprise-grade, tamper-proof, centralized audit trail recording all security, lifecycle, marks, and evaluation events:
- **Comprehensive Event Capture**:
  - `EXAM_CREATED`, `EXAM_UPDATED`, `EXAM_PUBLISHED`, `REEVALUATION_OPENED`, `REEVALUATION_CLOSED`, `EXAM_ARCHIVED`
  - `MARK_RECORDED`, `STUDENT_MARKS_RECORDED`, `MARKS_REVISED`
  - `REQUEST_SUBMITTED`, `REQUEST_UNDER_REVIEW`
  - `REVIEW_COMPLETED`
- **Structured Audit Metadata**:
  - `action`: Specific operation code.
  - `resourceType`: Target entity domain (`EXAM`, `QUESTION`, `MARKS`, `REQUEST`, `REVIEW`, `USER`, `SYSTEM`).
  - `resourceId`: Database primary key of the affected entity.
  - `previousValue`: State/score prior to operation.
  - `updatedValue`: State/score following operation.
  - `user`: Authenticated actor who initiated the event (or SYSTEM).
  - `timestamp`: Chronological creation timestamp (`updatable = false`).
- **Administrative Interface (`/admin/audit-logs`)**:
  - Role-protected: strictly restricted to `ROLE_ADMIN`.
  - Multi-criteria filtering: by Action, Resource Type, and User.
  - Chronological pagination and reverse chronological sorting.
- **Audit Immutability**:
  - Database schema forbids updating timestamps.
  - Normal users (students, faculty) have zero access to audit log endpoints or modification APIs.
  - No sensitive credentials, passwords, or authentication tokens are ever logged.

---

## 2. Architectural Design & Implementation

### 2.1 Enhanced AuditLog Entity (`AuditLog.java`)
Extended with indexed metadata fields:
- `resourceType` (`VARCHAR(50)`, indexed)
- `resourceId` (`BIGINT`)
- `previousValue` (`TEXT`)
- `updatedValue` (`TEXT`)
- Composite indexes on `(user_id)`, `(timestamp)`, `(action)`, and `(resource_type)`.

### 2.2 Dynamic Filtering Repository (`AuditLogRepository.java`)
Implemented custom parameterized JPQL query with `@EntityGraph(attributePaths = {"user"})` to eliminate $N+1$ query overhead:
```sql
SELECT a FROM AuditLog a WHERE 
(:action IS NULL OR a.action = :action) AND 
(:resourceType IS NULL OR a.resourceType = :resourceType) AND 
(:userId IS NULL OR a.user.id = :userId) 
ORDER BY a.timestamp DESC
```

### 2.3 Reusable Audit Service (`AuditService.java`)
- `log(user, action, description)`: General purpose logging.
- `log(user, action, resourceType, resourceId, previousValue, updatedValue, description)`: Fully structured audit recording.
- `filterLogs(action, resourceType, userId)`: Multi-criteria administrative filtering.

### 2.4 User Interface
- **`templates/admin/audit-logs.html`**: Filter bar with Action selector, Resource selector, and User dropdown, plus an audit table displaying timestamp, actor email, action badge, resource badge with ID, and previous/new value differentials.

---

## 3. Files Created & Modified

| File Path | Action | Description |
|---|---|---|
| `entity/AuditLog.java` | Modified | Added structured fields (`resourceType`, `resourceId`, `previousValue`, `updatedValue`) and indexes. |
| `repository/AuditLogRepository.java` | Modified | Added `@EntityGraph` and dynamic multi-criteria `filterLogs` JPQL query. |
| `service/AuditService.java` | Modified | Added overloaded structured logging and filter methods. |
| `controller/AdminController.java` | Modified | Added request parameters (`action`, `resourceType`, `userId`) to `/admin/audit-logs`. |
| `templates/admin/audit-logs.html` | Modified | Added multi-criteria filter form and resource/value change display. |
| `test/.../service/AuditTrailTests.java` | Created | 5 automated tests verifying structured logging, action filtering, resource filtering, user filtering, and chronological order. |

---

## 4. Testing & Verification

Executed `AuditTrailTests` via Maven Surefire:
1. `testCreateStructuredAuditLog`: Verified creation of complete structured audit log with resource, IDs, and value diffs.
2. `testFilterAuditLogsByAction`: Verified filtering logs by action code (`EXAM_CREATED`, `MARKS_REVISED`).
3. `testFilterAuditLogsByResourceType`: Verified filtering by resource (`EXAM`, `REQUEST`).
4. `testFilterAuditLogsByUser`: Verified isolating logs initiated by specific students or faculty.
5. `testChronologicalOrdering`: Verified latest events appear first.

**Test Results**: 5 tests run, 0 failures, 0 errors, 0 skipped.

---

## 5. Exit Criteria Verification

- [x] All critical application activities create structured audit records.
- [x] Administrators can inspect and filter audit history by action, resource, and actor.
- [x] Immutability and security protection prevent normal users from modifying or accessing audit data.
- [x] All 5 automated audit tests passed with 100% success rate.
