# Tasks: Phase II – Full-Stack Web Application

**Feature ID**: 001-fullstack-web-app
**Phase**: Phase II
**Created**: January 4, 2026
**Status**: Task Breakdown Complete

---

## Executive Summary

**Total Tasks**: 35
**Phases**: 6 (Setup, Foundation, US1, US2, US3-4, Validation)
**User Stories**: 4 (all P1 priority)
**Parallelizable Tasks**: 12 [P]
**Independent Test Criteria**: Defined per user story

---

## Phase Structure

| Phase | Focus | User Story | Tasks | Dependencies |
|-------|-------|-----------|-------|--------------|
| **1** | Setup | N/A | 3 | None |
| **2** | Foundation | N/A | 7 | Phase 1 complete |
| **3** | US1: User Registration & Auth | P1 | 8 | Phase 2 complete |
| **4** | US2: Task CRUD Operations | P1 | 9 | Phase 3 complete |
| **5** | US3-4: Multi-User & JWT | P1 | 5 | Phase 4 complete |
| **6** | Validation & Polish | N/A | 3 | Phase 5 complete |

---

## Phase 1: Setup & Project Initialization

**Goal**: Initialize project structure, configure dependencies, setup CI/CD

**Independent Test**: Project scaffolding complete, dependencies installable, environment variables configured

### Tasks

- [ ] T001 Create phase2 project structure per plan.md (frontend/, backend/, src/, specs/)
- [ ] T002 [P] Create frontend/package.json with Next.js 16+, TypeScript, dependencies
- [ ] T003 [P] Create backend/requirements.txt with FastAPI, SQLModel, PyJWT, python-better-auth

**Completion Criteria**:
- All directories created
- Dependencies installed without errors
- .env.example created with required variables

---

## Phase 2: Foundation & Infrastructure

**Goal**: Setup authentication, database connection, API middleware

**Independent Test**: Database connection established, JWT middleware functional, API server starts

### Tasks

- [ ] T004 Create backend/.env.example with DATABASE_URL, JWT_SECRET, BETTER_AUTH_SECRET
- [ ] T005 [P] Create backend/src/config.py for environment variable loading
- [ ] T006 [P] Create backend/src/db/database.py for Neon PostgreSQL connection
- [ ] T007 Create backend/src/db/models.py with SQLModel table definitions for users and tasks
- [ ] T008 [P] Create backend/src/middleware/auth.py for JWT validation middleware
- [ ] T009 [P] Create frontend/src/utils/auth.ts for token storage/retrieval
- [ ] T010 [P] Create frontend/src/utils/api-client.ts for fetch wrapper with JWT attachment

**Completion Criteria**:
- Database tables created (users, tasks)
- JWT middleware validates tokens and extracts user_id
- API client automatically attaches JWT to requests
- Environment variables loaded correctly

---

## Phase 3: User Story 1 – User Registration & First Task

**User Story**: New user signs up, authenticates, and creates their first task

**Priority**: P1 (Core feature enabling multi-user support)

**Independent Test**:
- User can signup with Better Auth
- JWT token issued and stored
- User can create first task
- Task persists in database
- Task visible only to authenticated user

### Tasks

- [ ] T011 [US1] Create backend/src/models/user.py with User SQLModel
- [ ] T012 [P] [US1] Create backend/src/models/task.py with Task SQLModel (user_id foreign key)
- [ ] T013 [P] [US1] Create backend/src/schemas/user.py with Pydantic schemas
- [ ] T014 [P] [US1] Create backend/src/schemas/task.py with TaskCreate, TaskRead schemas
- [ ] T015 [US1] Create backend/src/services/task_service.py with create_task(user_id, title, desc)
- [ ] T016 [P] [US1] Create frontend/src/app/auth/signup/page.tsx with Better Auth form
- [ ] T017 [P] [US1] Create frontend/src/app/auth/login/page.tsx with Better Auth form
- [ ] T018 [US1] Create POST /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py

**Completion Criteria**:
- User signup form functional
- JWT token issued and stored in localStorage
- Task creation form works
- Task stored in database with correct user_id
- No other user can view this task

---

## Phase 4: User Story 2 – Task CRUD Operations

**User Story**: Authenticated user manages tasks through web UI (create, read, update, delete, toggle)

**Priority**: P1 (Implements all 5 core features)

**Independent Test**:
- Task creation works
- Task list displays correct tasks
- Task edit updates database
- Task deletion removes from database
- Toggle changes status

### Tasks

- [ ] T019 [P] [US2] Create GET /api/{user_id}/tasks endpoint (list all tasks)
- [ ] T020 [P] [US2] Create GET /api/{user_id}/tasks/{id} endpoint (get single task)
- [ ] T021 [P] [US2] Create PUT /api/{user_id}/tasks/{id} endpoint (update task)
- [ ] T022 [P] [US2] Create DELETE /api/{user_id}/tasks/{id} endpoint (delete task)
- [ ] T023 [P] [US2] Create PATCH /api/{user_id}/tasks/{id}/complete endpoint (toggle status)
- [ ] T024 [US2] Create backend/src/services/task_service.py methods: list, get, update, delete, toggle
- [ ] T025 [P] [US2] Create frontend/src/components/TaskList.tsx to display user's tasks
- [ ] T026 [P] [US2] Create frontend/src/components/TaskForm.tsx for create/edit
- [ ] T027 [US2] Create frontend/src/app/dashboard/page.tsx with TaskList and create button

**Completion Criteria**:
- All 5 CRUD operations functional
- Frontend displays tasks correctly
- Edit/delete/toggle work
- No database errors
- Changes persist across page refresh

---

## Phase 5: User Story 3-4 – Multi-User Isolation & JWT Security

**User Stories**:
- US3: Multi-user data isolation (User A cannot see User B's tasks)
- US4: JWT authentication enforced (401 on missing/invalid token, 403 on user_id mismatch)

**Priority**: P1 (Core security requirement)

**Independent Test**:
- User A's JWT cannot access User B's tasks
- Request without JWT returns 401
- Expired JWT returns 401
- User ID mismatch returns 403
- Each user sees only their tasks

### Tasks

- [ ] T028 [P] [US3] Add authorization check in all endpoints: validate URL user_id == JWT user_id
- [ ] T029 [P] [US3] Update task_service.py: all queries include WHERE user_id = ?
- [ ] T030 [US3] Create frontend/src/components/AuthGuard.tsx for protected routes
- [ ] T031 [P] [US4] Create frontend/src/app/dashboard/layout.tsx (protected layout using AuthGuard)
- [ ] T032 [US4] Implement API client error handling: 401 → redirect to login, 403 → show error

**Completion Criteria**:
- User A cannot list User B's tasks (403 Forbidden)
- User A cannot update User B's task (403 Forbidden)
- User A cannot delete User B's task (403 Forbidden)
- Missing JWT returns 401 Unauthorized
- Expired JWT returns 401 Unauthorized
- Each user's task list contains only their tasks

---

## Phase 6: Validation, Integration & Polish

**Goal**: Validate end-to-end workflows, ensure security, document deployment

**Independent Test**: Full JWT flow functional, all user stories pass independent tests, data persists across sessions

### Tasks

- [ ] T033 Validate end-to-end JWT flow: signup → login → task creation → task visible
- [ ] T034 [P] Validate data persistence: create task → logout → login → task still visible
- [ ] T035 Create phase2/README.md with setup instructions, API documentation, deployment guide

**Completion Criteria**:
- All success criteria from spec.md verified
- No hardcoded secrets
- All endpoints require JWT
- User isolation enforced
- Data persists in PostgreSQL

---

## Task Dependency Graph

```
Phase 1 (Setup)
  ├─ T001: Project structure
  ├─ T002: Frontend package.json
  └─ T003: Backend requirements.txt
        ↓
Phase 2 (Foundation) - BLOCKING all user stories
  ├─ T004: .env.example
  ├─ T005: Config (env loading)
  ├─ T006: Database connection
  ├─ T007: SQLModel definitions
  ├─ T008: JWT middleware
  ├─ T009: Token storage
  └─ T010: API client
        ↓
Phase 3 (US1: Registration & First Task) - BLOCKING T016, T017
  ├─ T011: User model
  ├─ T012: Task model
  ├─ T013: User schemas
  ├─ T014: Task schemas
  ├─ T015: create_task service
  ├─ T016: Signup page
  ├─ T017: Login page
  └─ T018: POST /api/{user_id}/tasks
        ↓
Phase 4 (US2: CRUD Operations) - Depends on US1
  ├─ T019: GET /api/{user_id}/tasks
  ├─ T020: GET /api/{user_id}/tasks/{id}
  ├─ T021: PUT /api/{user_id}/tasks/{id}
  ├─ T022: DELETE /api/{user_id}/tasks/{id}
  ├─ T023: PATCH /api/{user_id}/tasks/{id}/complete
  ├─ T024: Service methods
  ├─ T025: TaskList component
  ├─ T026: TaskForm component
  └─ T027: Dashboard page
        ↓
Phase 5 (US3-4: Security & Isolation) - Depends on US2
  ├─ T028: Authorization validation
  ├─ T029: Query filtering
  ├─ T030: AuthGuard component
  ├─ T031: Protected layout
  └─ T032: Error handling
        ↓
Phase 6 (Validation & Polish)
  ├─ T033: E2E JWT flow
  ├─ T034: Data persistence
  └─ T035: Documentation
```

---

## Parallel Execution Examples

### Phase 2 Parallelization

These tasks can run in parallel (no dependencies):

```
- T005 [P] Create backend/src/config.py
- T006 [P] Create backend/src/db/database.py
- T008 [P] Create backend/src/middleware/auth.py
- T009 [P] Create frontend/src/utils/auth.ts
- T010 [P] Create frontend/src/utils/api-client.ts

Execution: Start all 5 simultaneously, complete Phase 2 faster
```

### Phase 3 Parallelization

These tasks can run in parallel:

```
- T011 [P] Create User model
- T012 [P] Create Task model
- T013 [P] Create User schemas
- T014 [P] Create Task schemas
- T016 [P] Create signup page
- T017 [P] Create login page

Then sequentially:
- T015: create_task service (depends on T012)
- T018: POST endpoint (depends on T015)
```

### Phase 4 Parallelization

API endpoints can be implemented in parallel:

```
- T019 [P] GET /api/{user_id}/tasks
- T020 [P] GET /api/{user_id}/tasks/{id}
- T021 [P] PUT /api/{user_id}/tasks/{id}
- T022 [P] DELETE /api/{user_id}/tasks/{id}
- T023 [P] PATCH /api/{user_id}/tasks/{id}/complete

Frontend components in parallel:
- T025 [P] TaskList component
- T026 [P] TaskForm component

Then:
- T027: Dashboard page (depends on T025, T026)
```

---

## Implementation Strategy

### MVP Scope (Recommended Starting Point)

**Phase 1 + Phase 2 + US1 Only** = Minimal Viable Product

This gives you:
- User signup/login
- First task creation
- JWT-protected API
- Database persistence

**Tasks**: T001-T018 (18 tasks)

**Time to MVP**: ~2 hours with Claude Code

### Incremental Delivery Path

1. **Sprint 1 (MVP)**: Phases 1-3 (T001-T018)
   - User can signup, login, create task
   - JWT authentication working
   - Task stored in database

2. **Sprint 2**: Phase 4 (T019-T027)
   - Full CRUD operations
   - Task list display
   - Edit/delete/toggle working

3. **Sprint 3**: Phase 5 (T028-T032)
   - Multi-user isolation enforced
   - Security hardening
   - Protected routes

4. **Sprint 4**: Phase 6 (T033-T035)
   - End-to-end validation
   - Documentation
   - Deployment guide

---

## Independent Test Criteria by User Story

### US1: Registration & First Task
```
✓ User can sign up with email/password
✓ JWT token issued and stored
✓ User can log in with credentials
✓ User can create task with title
✓ Task appears in database
✓ Task persists after logout/login
```

### US2: Task CRUD Operations
```
✓ Task list shows user's tasks
✓ User can edit task title/description
✓ User can delete task
✓ User can mark task complete
✓ User can toggle status back to incomplete
✓ Changes persist in database
```

### US3: Multi-User Isolation
```
✓ User A cannot list User B's tasks (403)
✓ User A cannot read User B's task (403)
✓ User A cannot update User B's task (403)
✓ User A cannot delete User B's task (403)
✓ User A's list shows only User A's tasks
✓ User B's list shows only User B's tasks
```

### US4: JWT Security
```
✓ Request without JWT returns 401
✓ Request with expired JWT returns 401
✓ Request with invalid JWT returns 401
✓ URL user_id != JWT user_id → 403
✓ Valid JWT allows request to proceed
✓ Token includes user_id and expiry claims
```

---

## Validation Checklist

### Backend Validation

- [ ] All endpoints require Authorization header
- [ ] JWT middleware validates signature on every request
- [ ] user_id mismatch returns 403 Forbidden
- [ ] Missing JWT returns 401 Unauthorized
- [ ] All queries filtered by user_id
- [ ] No cross-user data access possible
- [ ] Error responses are JSON with safe messages
- [ ] Database persists all data correctly

### Frontend Validation

- [ ] JWT token stored securely (localStorage or HttpOnly cookie)
- [ ] API client attaches JWT to every request
- [ ] Protected routes redirect to login if no token
- [ ] Login/signup forms functional
- [ ] Task list displays only authenticated user's tasks
- [ ] CRUD operations trigger API calls
- [ ] Error messages are user-friendly
- [ ] UI responds within 2 seconds

### Integration Validation

- [ ] User can complete full signup → login → create task workflow
- [ ] Task created in one session appears after logout/login
- [ ] Concurrent users don't see each other's tasks
- [ ] API returns correct HTTP status codes
- [ ] Database indexes on user_id for performance
- [ ] No hardcoded secrets in code

---

## Notes

### Task Sequencing

- **Setup (Phase 1)**: 3 tasks, must complete first
- **Foundation (Phase 2)**: 7 tasks, must complete before any user story
- **User Stories (Phases 3-5)**: 22 tasks organized by story priority
- **Validation (Phase 6)**: 3 tasks, ensure everything works together

### Parallelization Opportunities

- **12 tasks marked [P]** can run in parallel if dependencies resolved
- **Phase 2 fully parallelizable** (5/7 tasks can run simultaneously)
- **Phase 3 partially parallelizable** (6 model/schema tasks can run simultaneously)
- **Phase 4 fully parallelizable** (API endpoints can be implemented independently)

### No Manual Coding

All tasks are specified precisely for Claude Code generation:
- Clear file paths
- Required function signatures
- Input/output contracts
- Dependencies listed

### Security-First Approach

Every task includes security considerations:
- JWT validation on all endpoints
- user_id verification in middleware
- Query filtering in services
- Error message sanitization

---

## Completion Definition

Phase II tasks are complete when:

1. ✅ All 35 tasks completed
2. ✅ User can signup → login → create task → view task → edit task → delete task
3. ✅ JWT authentication enforced on all API endpoints
4. ✅ User isolation prevents cross-user access
5. ✅ Data persists in PostgreSQL
6. ✅ No hardcoded secrets
7. ✅ All success criteria from spec.md verified
8. ✅ End-to-end integration tests pass

---

**Task Breakdown Status**: Complete
**Total Tasks**: 35
**Parallelizable**: 12
**Ready for**: Claude Code implementation via `/sp.implement`
**Created**: January 4, 2026
