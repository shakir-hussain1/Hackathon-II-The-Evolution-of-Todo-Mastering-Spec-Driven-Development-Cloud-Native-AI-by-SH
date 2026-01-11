# Feature Specification: Phase II – Full-Stack Web Application

**Feature ID**: 001-fullstack-web-app
**Phase**: Phase II
**Created**: January 4, 2026
**Status**: Draft
**Project**: Hackathon II – The Evolution of Todo

---

## Executive Summary

Transform the Phase I in-memory Python console Todo application into a secure, full-stack web application with persistent storage, multi-user support, and REST API. All five core task management features (create, read, update, delete, toggle complete) must work through a responsive web interface backed by a PostgreSQL database with JWT authentication.

---

## User Scenarios & Testing

### User Story 1 - User Registration and First Task (Priority: P1)

New user signs up, authenticates, and creates their first task.

**Why this priority**: Core feature enabling multi-user support and data persistence.

**Independent Test**: User can sign up, log in, create a task, see it in list, and logout. Task persists after re-login.

**Acceptance Scenarios**:

1. **Given** user is on signup page, **When** user enters email and password, **Then** account is created and user is authenticated
2. **Given** user is authenticated, **When** user navigates to dashboard, **Then** empty task list is displayed
3. **Given** authenticated user, **When** user creates task "Buy groceries", **Then** task appears in list with status "incomplete"
4. **Given** task created in session, **When** user logs out and logs back in, **Then** task still exists with same data

---

### User Story 2 - Task CRUD Operations (Priority: P1)

Authenticated user manages their tasks through web UI.

**Why this priority**: Implements all 5 core features required.

**Independent Test**: All CRUD operations (create, read, update, delete, toggle) work independently and persist.

**Acceptance Scenarios**:

1. **Given** authenticated user with tasks, **When** user clicks task to edit, **Then** edit form appears with current values
2. **Given** edit form displayed, **When** user changes title to "New title" and submits, **Then** task is updated and list reflects change
3. **Given** task in list, **When** user clicks delete button, **Then** task is removed from list and database
4. **Given** task with "incomplete" status, **When** user toggles completion, **Then** status changes to "complete"
5. **Given** multiple incomplete tasks, **When** user marks some complete, **Then** completed tasks show correct status

---

### User Story 3 - Multi-User Data Isolation (Priority: P1)

Each user sees and can only modify their own tasks. Cross-user access is prevented.

**Why this priority**: Security requirement preventing data leakage between users.

**Independent Test**: User A cannot see, edit, or delete User B's tasks even if they know task ID.

**Acceptance Scenarios**:

1. **Given** User A is logged in, **When** User A attempts to access `/api/users/user-b-id/tasks`, **Then** request returns 403 Forbidden
2. **Given** two users with same task titles, **When** each logs in, **Then** each sees only their own tasks
3. **Given** User A knows User B's task ID, **When** User A attempts DELETE on that task, **Then** request returns 403 Forbidden

---

### User Story 4 - JWT Authentication (Priority: P1)

API requires valid JWT token on every request. Unauthenticated requests are rejected.

**Why this priority**: Core security requirement for multi-user system.

**Independent Test**: API endpoints reject requests without JWT token or with invalid token.

**Acceptance Scenarios**:

1. **Given** request without Authorization header, **When** user calls any API endpoint, **Then** returns 401 Unauthorized
2. **Given** expired JWT token, **When** user makes request, **Then** returns 401 Unauthorized
3. **Given** valid JWT token, **When** user makes request with token in Authorization header, **Then** request succeeds
4. **Given** JWT token from User A, **When** token is used to access User B's tasks, **Then** user_id mismatch returns 403

---

### Edge Cases

- What happens when user tries to create task with empty title? → Validation error returned
- How does system handle simultaneous updates to same task? → Last write wins
- What happens if user deletes all tasks? → Task list shows "No tasks" message
- How does UI handle network timeout on task creation? → Error message shown, user can retry

---

## Requirements

### API Endpoint Requirements

**REQ-API-001: Create Task**
- Endpoint: `POST /api/{user_id}/tasks`
- Headers: `Authorization: Bearer <jwt_token>`
- Body: `{ "title": "string", "description": "string (optional)" }`
- Success Response: 201 Created with task object including id, status, created_at
- Error: 400 if title is empty, 401 if no token, 403 if user_id mismatch

**REQ-API-002: List Tasks**
- Endpoint: `GET /api/{user_id}/tasks`
- Headers: `Authorization: Bearer <jwt_token>`
- Query: Optional filter by status (incomplete/complete)
- Response: 200 OK with array of task objects
- Error: 401 if no token, 403 if user_id mismatch

**REQ-API-003: Get Single Task**
- Endpoint: `GET /api/{user_id}/tasks/{id}`
- Headers: `Authorization: Bearer <jwt_token>`
- Response: 200 OK with task object
- Error: 401 if no token, 403 if user_id mismatch, 404 if task not found

**REQ-API-004: Update Task**
- Endpoint: `PUT /api/{user_id}/tasks/{id}`
- Headers: `Authorization: Bearer <jwt_token>`
- Body: `{ "title": "string (optional)", "description": "string (optional)" }`
- Response: 200 OK with updated task object
- Error: 401 if no token, 403 if user_id mismatch, 404 if task not found

**REQ-API-005: Delete Task**
- Endpoint: `DELETE /api/{user_id}/tasks/{id}`
- Headers: `Authorization: Bearer <jwt_token>`
- Response: 204 No Content
- Error: 401 if no token, 403 if user_id mismatch, 404 if task not found

**REQ-API-006: Toggle Task Completion**
- Endpoint: `PATCH /api/{user_id}/tasks/{id}/complete`
- Headers: `Authorization: Bearer <jwt_token>`
- Response: 200 OK with updated task showing new status
- Error: 401 if no token, 403 if user_id mismatch, 404 if task not found

### Authentication Requirements

**REQ-AUTH-001**: System uses Better Auth for user signup/login
**REQ-AUTH-002**: Better Auth issues JWT token containing user_id
**REQ-AUTH-003**: JWT token passed in `Authorization: Bearer <token>` header
**REQ-AUTH-004**: Backend validates JWT signature on every API request
**REQ-AUTH-005**: Expired or invalid tokens return HTTP 401 Unauthorized
**REQ-AUTH-006**: user_id in URL must match authenticated user_id (HTTP 403 if mismatch)

### Frontend Requirements

**REQ-FE-001**: Responsive design works on desktop, tablet, mobile
**REQ-FE-002**: Authentication pages (signup, login) integrated with Better Auth
**REQ-FE-003**: Dashboard displays list of user's tasks with status indicators
**REQ-FE-004**: Create task form with title (required) and description (optional) fields
**REQ-FE-005**: Edit task form allows updating title and description
**REQ-FE-006**: Delete button removes task after optional confirmation
**REQ-FE-007**: Toggle button or checkbox marks task complete/incomplete
**REQ-FE-008**: Logout button clears JWT token from storage
**REQ-FE-009**: All user actions communicate via REST API only (no direct database access)
**REQ-FE-010**: UI shows error messages for failed API requests

### Database Requirements

**REQ-DB-001**: PostgreSQL database (Neon Serverless) stores all persistent data
**REQ-DB-002**: SQLModel ORM used for all database operations
**REQ-DB-003**: Users table managed by Better Auth with fields: id, email, name, created_at
**REQ-DB-004**: Tasks table with fields:
   - id (integer, primary key, auto-increment)
   - user_id (string/UUID, foreign key, not null)
   - title (string, max 255, not null)
   - description (text, nullable)
   - status (enum: "incomplete" or "complete", default "incomplete")
   - created_at (timestamp, default now())
   - updated_at (timestamp, auto-update on modification)
**REQ-DB-005**: Unique constraint on (user_id, title) to prevent duplicate task names per user
**REQ-DB-006**: Foreign key enforces referential integrity between tasks and users

### Key Entities

- **User**: Represents authenticated user (managed by Better Auth)
  - id: unique identifier
  - email: user's email address
  - name: optional user name
  - created_at: account creation timestamp

- **Task**: Represents individual todo item
  - id: unique identifier
  - user_id: foreign key linking to owner
  - title: task description (max 255 characters)
  - description: optional detailed description
  - status: "incomplete" or "complete"
  - created_at: when task was created
  - updated_at: when task was last modified

---

## Success Criteria

### Functional Success

- **SC-001**: All 5 core features work via web UI (create, read, update, delete, toggle complete)
- **SC-002**: All API endpoints (POST, GET, PUT, DELETE, PATCH) return correct HTTP responses
- **SC-003**: Tasks created in one session persist after logout and re-login
- **SC-004**: User can filter task list by status (incomplete vs complete)
- **SC-005**: Form validation prevents empty task titles and shows error messages

### Security Success

- **SC-006**: Every API request without valid JWT token returns 401 Unauthorized
- **SC-007**: User attempting to access another user's tasks receives 403 Forbidden
- **SC-008**: JWT tokens are never visible in frontend code or browser console
- **SC-009**: No hardcoded secrets in source code (all in environment variables)
- **SC-010**: JWT signature verified on every backend request

### Data Integrity

- **SC-011**: Task data persists across application restarts
- **SC-012**: Each user sees only their own tasks (no cross-user leakage)
- **SC-013**: Concurrent updates don't cause data corruption (last write wins)
- **SC-014**: Deleted tasks are permanently removed from database

### User Experience

- **SC-015**: Web UI is responsive and usable on desktop (1920x1080), tablet (768x1024), mobile (375x667)
- **SC-016**: Task operations complete within 2 seconds
- **SC-017**: Error messages are user-friendly and explain what went wrong
- **SC-018**: Users don't need documentation to create/edit/delete tasks

### Code Quality

- **SC-019**: 100% of implementation generated by Claude Code (no manual coding)
- **SC-020**: Specification is sufficient for implementation without additional clarification

---

## Scope

### In Scope

- Full-stack web application (Next.js frontend + FastAPI backend)
- Multi-user support with JWT authentication via Better Auth
- Persistent PostgreSQL database (Neon Serverless)
- All 5 core features: create, read, update, delete, toggle complete
- Responsive web UI (desktop, tablet, mobile)
- REST API with proper error handling
- User data isolation (no cross-user access)
- SQLModel ORM for database operations

### Out of Scope

- Console/CLI interface (web only)
- In-memory storage (persistent database only)
- Chatbot or natural language interface
- Background jobs or task queues
- Role-based access control (single user role only)
- Offline-first support or service workers
- Mobile-native applications (responsive web only)
- Analytics, reporting, or data visualization dashboards
- Email notifications or external integrations
- Deployment or DevOps configuration
- Performance optimization beyond basic standards

---

## Constraints

### Technical Constraints

- **No console-only interaction**: All functionality must be through web UI
- **No in-memory storage**: All data must persist in PostgreSQL
- **No manual coding**: 100% AI-generated via Claude Code
- **No bypassing authentication**: Every API endpoint requires valid JWT
- **No hardcoded secrets**: All sensitive values in environment variables
- **No AI chatbot**: Phase II does not include chatbot features

### Technology Stack (Fixed)

- Frontend: Next.js 16+ with App Router, TypeScript
- Backend: Python FastAPI
- Database: PostgreSQL (Neon Serverless)
- ORM: SQLModel
- Authentication: Better Auth with JWT tokens
- Development: Claude Code + Spec-Kit Plus

### Deployment Assumptions

- Environment variables available for DATABASE_URL, JWT_SECRET, etc.
- Neon database connection stable
- Better Auth properly configured
- Frontend and backend can communicate without CORS issues

---

## Validation Rules

- Every requirement must be testable without implementation knowledge
- All API contracts explicitly defined with status codes
- Security rules must be explicit (JWT required, user_id validation, cross-user prevention)
- Edge cases documented with expected system behavior
- Success criteria measurable and technology-agnostic

---

## Next Steps

1. **Specification Review**: Validate spec completeness
2. **Planning** (`/sp.plan`): Create implementation plan from spec
3. **Task Breakdown** (`/sp.tasks`): Generate TDD task list
4. **Implementation** (`/sp.implement`): Generate code via Claude Code

---

**Specification Status**: Complete and Ready for Planning
**Created**: January 4, 2026
**Target**: Phase II – Full-Stack Web Application
