# Phase II Specification Overview

**Project**: Hackathon II – The Evolution of Todo
**Phase**: Phase II – Full-Stack Web Application
**Status**: Implementation Ready
**Created**: January 4, 2026

---

## Vision

Transform the Phase I in-memory console Todo application into a secure, multi-user, full-stack web application with persistent storage, REST API, and JWT authentication.

---

## Core Features

### Feature 1: User Authentication (Better Auth + JWT)
- User signup with email/password
- User login with credentials
- JWT token issuance (24-hour expiry)
- Secure token storage (HttpOnly cookie / localStorage)
- Protected API endpoints

### Feature 2: Task Management (CRUD)
- Create task (title + optional description)
- Read task (single or list)
- Update task (title/description)
- Delete task (permanent)
- Toggle task completion status

### Feature 3: Multi-User Data Isolation
- Each user sees only their tasks
- Cross-user access blocked (403 Forbidden)
- Database enforces user_id ownership

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | Next.js | 16+ |
| **Frontend** | React | 19+ |
| **Frontend** | TypeScript | 5.0+ |
| **Backend** | FastAPI | 0.110+ |
| **Backend** | Python | 3.10+ |
| **Backend** | SQLModel | 0.0.14+ |
| **Database** | PostgreSQL | 15+ (Neon) |
| **Auth** | Better Auth | Latest |
| **Auth** | PyJWT | 2.8+ |

---

## Architecture

### System Layers

```
┌─────────────────────────────────────────┐
│   Frontend (Next.js App Router)         │
│   - Pages: auth, dashboard               │
│   - Components: TaskList, TaskForm       │
│   - API Client: fetch + JWT attachment   │
└──────────────────┬──────────────────────┘
                   │ HTTP/REST
                   │ Authorization: Bearer <JWT>
                   ▼
┌─────────────────────────────────────────┐
│   Backend (FastAPI + SQLModel)          │
│   - Routes: /api/users/{user_id}/tasks  │
│   - Middleware: JWT validation          │
│   - Services: Business logic             │
│   - Models: User, Task                   │
└──────────────────┬──────────────────────┘
                   │ SQL/ORM
                   ▼
┌─────────────────────────────────────────┐
│   Database (Neon PostgreSQL)            │
│   - users table (Better Auth)           │
│   - tasks table (user_id scoped)        │
└─────────────────────────────────────────┘
```

---

## Key Specifications

### API Contract
- All endpoints require `Authorization: Bearer <jwt>`
- All endpoints scoped to `/api/users/{user_id}/...`
- All responses in JSON format
- HTTP status codes: 200, 201, 204, 400, 401, 403, 404, 500

### Database
- **users**: Managed by Better Auth
- **tasks**: id, user_id, title, description, status, created_at, updated_at

### Authentication
- JWT issued by Better Auth
- Token contains: user_id, exp, iat
- Signature verified on every request
- Expired/invalid tokens → 401 Unauthorized

---

## User Stories (All P1 Priority)

| Story | Title | Scope |
|-------|-------|-------|
| **US1** | User Registration & First Task | Signup, JWT, create 1 task |
| **US2** | Task CRUD Operations | All 5 operations functional |
| **US3** | Multi-User Isolation | Cross-user access blocked |
| **US4** | JWT Security | Authentication enforced |

---

## Validation Success Criteria

1. ✅ All 5 core features work via web UI
2. ✅ JWT authentication enforced on every endpoint
3. ✅ Users can only see/modify their own tasks
4. ✅ Data persists in PostgreSQL
5. ✅ 401 on missing/invalid JWT
6. ✅ 403 on user ID mismatch
7. ✅ No hardcoded secrets

---

## Related Documents

- **spec.md**: Detailed specification (user stories, requirements, success criteria)
- **plan.md**: Implementation plan (architecture, decisions, phases)
- **tasks.md**: Task breakdown (35 tasks organized by phase)
- **features/**: Feature specifications
- **api/**: API contracts
- **database/**: Schema definitions

---

**Status**: Ready for Implementation
**Next Step**: `/sp.implement`
