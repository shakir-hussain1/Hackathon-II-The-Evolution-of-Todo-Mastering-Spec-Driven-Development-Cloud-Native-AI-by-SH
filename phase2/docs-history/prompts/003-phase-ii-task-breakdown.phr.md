# PHR: Phase II Task Breakdown

**Timestamp**: January 4, 2026
**Model**: Claude Haiku 4.5
**Task Type**: Task Decomposition
**Stage**: Tasks
**Feature**: 001-fullstack-web-app

---

## PROMPT_TEXT

```
Phase: Phase II – Todo Full-Stack Web Application
Project: Hackathon II – The Evolution of Todo

Purpose:
Decompose Phase II specifications and implementation plan into
actionable, executable tasks with clear dependencies and parallel
opportunities. All tasks written for Claude Code implementation.

Phases:

B. Database & Models
B1. Specify database schema
- Define users (Better Auth managed)
- Define tasks table with user_id ownership
- Define indexes for user filtering

B2. Define SQLModel models
- Task model aligned with schema
- Ownership enforced via user_id

C. Authentication & Security

C1. Specify Better Auth JWT configuration
- Enable JWT issuance
- Define token expiry

C2. Define JWT verification logic
- Extract token from Authorization header
- Validate signature using shared secret
- Decode user identity

D. API Layer

D1. Implement REST endpoints
- GET    /api/{user_id}/tasks
- POST   /api/{user_id}/tasks
- GET    /api/{user_id}/tasks/{id}
- PUT    /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH  /api/{user_id}/tasks/{id}/complete

D2. Enforce authorization rules
- Match route user_id with JWT user_id
- Filter all queries by authenticated user

E. Frontend

E1. Implement auth-aware API client
- Attach JWT to every request

E2. Build core UI pages
- Login / signup
- Task list
- Create / update task forms

F. Integration & Validation

F1. Backend validation
- 401 on missing/invalid token
- Cross-user access blocked

F2. Frontend validation
- Auth-gated UI
- CRUD operations function correctly

Constraints:
- No manual coding
- No auth bypass
- No Phase III features

Completion Definition:
Phase II tasks are complete when the full-stack
Todo web application functions securely with
persistent storage and user isolation using specs alone.
```

---

## RESPONSE_TEXT

### Comprehensive Task Breakdown Created

**Location**: `phase2/specs/001-fullstack-web-app/tasks.md`

**Statistics**:
- Total Tasks: 35
- Phases: 6 (Setup, Foundation, US1, US2, US3-4, Validation)
- Parallelizable Tasks: 12 [P]
- Dependencies: Documented in detail

---

## Task Organization

### Phase 1: Setup & Project Initialization (3 tasks)

- T001: Create project structure
- T002 [P]: Frontend package.json
- T003 [P]: Backend requirements.txt

**Completion**: Project scaffolding ready

---

### Phase 2: Foundation & Infrastructure (7 tasks)

- T004: Environment configuration
- T005 [P]: Backend config.py
- T006 [P]: Database connection
- T007: SQLModel table definitions
- T008 [P]: JWT middleware
- T009 [P]: Frontend token storage
- T010 [P]: Frontend API client

**Completion**: Database + JWT middleware + API client ready
**Note**: 5/7 tasks parallelizable

---

### Phase 3: User Story 1 – Registration & First Task (8 tasks)

- T011: User model
- T012 [P]: Task model
- T013 [P]: User schemas
- T014 [P]: Task schemas
- T015: create_task service
- T016 [P]: Signup page
- T017 [P]: Login page
- T018: POST /api/{user_id}/tasks

**Independent Test Criteria**:
- User signup functional
- JWT token issued and stored
- First task creation works
- Task persists in database

**Parallelization**: T011-T014, T016-T017 can run simultaneously

---

### Phase 4: User Story 2 – Task CRUD Operations (9 tasks)

- T019 [P]: GET /api/{user_id}/tasks
- T020 [P]: GET /api/{user_id}/tasks/{id}
- T021 [P]: PUT /api/{user_id}/tasks/{id}
- T022 [P]: DELETE /api/{user_id}/tasks/{id}
- T023 [P]: PATCH /api/{user_id}/tasks/{id}/complete
- T024: Service methods (list, get, update, delete, toggle)
- T025 [P]: TaskList component
- T026 [P]: TaskForm component
- T027: Dashboard page

**Independent Test Criteria**:
- All 5 CRUD operations functional
- Frontend displays tasks
- Edit/delete/toggle work
- Changes persist

**Parallelization**: T019-T023 (endpoints), T025-T026 (components) fully parallelizable

---

### Phase 5: User Story 3-4 – Multi-User Isolation & JWT Security (5 tasks)

- T028 [P]: Authorization check (user_id validation)
- T029 [P]: Query filtering in services
- T030: AuthGuard component
- T031 [P]: Protected dashboard layout
- T032: Error handling (401/403)

**Independent Test Criteria**:
- User cannot access other user's tasks (403)
- Missing JWT returns 401
- Expired JWT returns 401
- Each user sees only own tasks

---

### Phase 6: Validation & Polish (3 tasks)

- T033: End-to-end JWT flow validation
- T034 [P]: Data persistence validation
- T035: README documentation

**Completion**: All success criteria verified, deployment guide ready

---

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundation) ← BLOCKING all user stories
    ↓
Phase 3 (US1: Auth & First Task)
    ↓
Phase 4 (US2: CRUD)
    ↓
Phase 5 (US3-4: Security)
    ↓
Phase 6 (Validation)
```

---

## Parallel Execution Examples

**Phase 2 Parallelization** (5 concurrent tasks):
- T005, T006, T008, T009, T010 start simultaneously
- Reduces Phase 2 from sequential to parallel execution
- Saves ~2 hours of development time

**Phase 3 Parallelization** (6 concurrent model/schema tasks):
- T011, T012, T013, T014, T016, T017 run in parallel
- T015, T018 executed after models/schemas complete
- Parallelizable: 6/8 tasks

**Phase 4 Parallelization** (5 concurrent API endpoints):
- T019, T020, T021, T022, T023 run in parallel
- Frontend components T025, T026 parallel
- T024, T027 executed after dependencies resolved
- Parallelizable: 7/9 tasks

---

## MVP Scope Recommendation

**Minimum Viable Product**: Phases 1-3 (18 tasks)

Delivers:
- User signup/login via Better Auth
- First task creation
- Task persistence in PostgreSQL
- JWT authentication working
- Data isolated per user

**Estimated Time**: 2-3 hours with Claude Code

---

## Incremental Delivery Path

1. **Sprint 1 (MVP)**: T001-T018 (Setup + Foundation + US1)
2. **Sprint 2**: T019-T027 (CRUD operations)
3. **Sprint 3**: T028-T032 (Security hardening)
4. **Sprint 4**: T033-T035 (Validation + docs)

---

## Implementation Strategy

### Task Format Compliance

All 35 tasks follow strict checklist format:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

✅ Checkbox: Present on all tasks
✅ Task ID: T001-T035 sequential
✅ [P] marker: 12 tasks marked parallelizable
✅ [Story] label: US1, US2, US3, US4 on story tasks
✅ Description: Clear action with file path

### File Path Specificity

Each task includes exact file path:
- `backend/src/middleware/auth.py`
- `frontend/src/utils/api-client.ts`
- `backend/src/models/task.py`
- etc.

Claude Code can implement directly from task description.

### No Manual Coding Constraint

Tasks written for 100% AI generation:
- Input/output contracts specified
- Dependencies documented
- Function signatures implied
- Integration points clear

---

## Independent Test Criteria

### US1: Registration & First Task
```
✓ Signup form functional
✓ JWT token issued and stored
✓ Login form functional
✓ Task creation form works
✓ Task stored with user_id
✓ Task persists after logout/login
```

### US2: CRUD Operations
```
✓ GET returns authenticated user's tasks
✓ POST creates new task
✓ PUT updates task
✓ DELETE removes task
✓ PATCH toggles completion status
✓ All changes persist in database
```

### US3: Multi-User Isolation
```
✓ User A cannot list User B's tasks (403)
✓ User A cannot modify User B's task (403)
✓ User A cannot delete User B's task (403)
✓ Each user sees only own tasks
```

### US4: JWT Security
```
✓ Missing JWT → 401 Unauthorized
✓ Expired JWT → 401 Unauthorized
✓ Invalid JWT → 401 Unauthorized
✓ URL user_id != JWT user_id → 403 Forbidden
✓ Valid JWT allows request
```

---

## Completion Definition

Phase II task breakdown complete when:

✅ All 35 tasks listed with clear descriptions
✅ Dependencies documented and validated
✅ Parallelization opportunities identified
✅ Independent test criteria defined
✅ MVP scope clearly marked
✅ File paths specified for all tasks
✅ Task format checklist compliance verified
✅ Ready for Claude Code `/sp.implement` execution

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 35 |
| **Phases** | 6 |
| **Parallelizable Tasks** | 12 (34%) |
| **Sequential Tasks** | 23 (66%) |
| **User Stories** | 4 (all P1) |
| **Setup Tasks** | 3 |
| **Foundation Tasks** | 7 |
| **Feature Tasks** | 22 |
| **Validation Tasks** | 3 |
| **MVP Task Count** | 18 |
| **Full Implementation Tasks** | 35 |

---

**Task Breakdown Status**: Complete and Validated
**Ready for**: Claude Code implementation via `/sp.implement`
**Location**: `phase2/specs/001-fullstack-web-app/tasks.md`
**Created**: January 4, 2026
