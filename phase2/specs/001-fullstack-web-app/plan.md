# Implementation Plan: Phase II – Full-Stack Web Application

**Feature ID**: 001-fullstack-web-app
**Phase**: Phase II
**Created**: January 4, 2026
**Status**: In Planning

---

## 1. Architecture Sketch

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│               Frontend (Next.js 16+)                    │
│  - App Router pages (layout, auth, dashboard)           │
│  - React components (TaskList, TaskForm, Header)        │
│  - API client (fetch wrapper + JWT attachment)          │
│  - Auth-aware rendering (protected routes)              │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST
                       │ Authorization: Bearer <JWT>
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Backend (FastAPI)                          │
│  - Routes (/api/users/{user_id}/tasks)                  │
│  - JWT Middleware (validate token + user_id)            │
│  - Service Layer (business logic)                       │
│  - ORM Layer (SQLModel + Pydantic)                      │
└──────────────────────┬──────────────────────────────────┘
                       │ SQL/ORM
                       ▼
┌─────────────────────────────────────────────────────────┐
│        Database (Neon PostgreSQL)                       │
│  - users table (Better Auth managed)                    │
│  - tasks table (user_id scoped)                         │
│  - Constraints & indexes for performance                │
└─────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
1. User Signs Up/Logs In
   ├─ Frontend: User enters credentials
   ├─ Better Auth: Validates credentials
   ├─ JWT Issued: Token contains {user_id, exp, iat}
   └─ Frontend: Stores JWT in secure storage

2. API Request
   ├─ Frontend: Attaches JWT to Authorization header
   ├─ Backend: Receives request
   ├─ JWT Middleware: Validates signature + expiry
   ├─ Extract: user_id from JWT claims
   ├─ Validate: URL user_id == JWT user_id
   └─ Route Handler: Executes if authorized

3. Database Query
   ├─ Service Layer: Builds query
   ├─ WHERE Clause: user_id = authenticated_user_id
   └─ Returns: Only authenticated user's data
```

### Separation of Concerns

| Layer | Responsibility | Technologies |
|-------|---|---|
| **Frontend** | UI rendering, API calls, auth state | Next.js, React, TypeScript |
| **API Client** | Attach JWT, handle errors, retry logic | Fetch API wrapper |
| **Backend Routes** | HTTP methods, input validation | FastAPI, Pydantic |
| **Auth Middleware** | JWT verification, user_id matching | Better Auth, PyJWT |
| **Service Layer** | Business logic, data transformations | Python async functions |
| **ORM** | Database abstractions, model validation | SQLModel, SQLAlchemy |
| **Database** | Persistence, constraints, indexes | PostgreSQL (Neon) |
| **Agents & Skills** | Reusable intelligence, validation logic | Custom Python modules |

---

## 2. Repository & Section Structure Plan

### Monorepo Organization

```
phase2/
├── specs/
│   └── 001-fullstack-web-app/
│       ├── spec.md                 # Feature specification
│       ├── plan.md                 # This implementation plan
│       ├── research.md             # Research findings
│       ├── data-model.md           # Entity definitions
│       └── contracts/              # API contracts
│           ├── tasks-endpoints.md
│           └── auth-flow.md
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js App Router
│   │   │   ├── layout.tsx          # Root layout
│   │   │   ├── page.tsx            # Home/landing
│   │   │   ├── auth/
│   │   │   │   ├── signup/page.tsx
│   │   │   │   └── login/page.tsx
│   │   │   └── dashboard/
│   │   │       ├── layout.tsx      # Protected layout
│   │   │       ├── page.tsx        # Task list
│   │   │       └── tasks/[id]/edit/page.tsx
│   │   ├── components/             # React components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   ├── Header.tsx
│   │   │   └── AuthGuard.tsx
│   │   ├── hooks/                  # Custom hooks
│   │   │   └── useTasks.ts
│   │   ├── utils/
│   │   │   ├── api-client.ts       # JWT attachment + error handling
│   │   │   └── auth.ts             # Token storage/retrieval
│   │   └── styles/                 # Global styles
│   ├── CLAUDE.md                   # Frontend guidelines
│   ├── package.json
│   └── tsconfig.json
├── backend/
│   ├── src/
│   │   ├── main.py                 # FastAPI app
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── tasks.py        # Task endpoints
│   │   ├── models/
│   │   │   ├── user.py             # User model
│   │   │   └── task.py             # Task model
│   │   ├── schemas/
│   │   │   ├── user.py             # Pydantic schemas
│   │   │   └── task.py
│   │   ├── services/
│   │   │   └── task_service.py     # Business logic
│   │   ├── db/
│   │   │   ├── database.py         # Connection + session
│   │   │   └── models.py           # SQLModel definitions
│   │   ├── middleware/
│   │   │   └── auth.py             # JWT validation middleware
│   │   └── config.py               # Environment config
│   ├── CLAUDE.md                   # Backend guidelines
│   ├── requirements.txt
│   └── pyproject.toml
├── src/
│   ├── agents/                     # Reusable agents
│   │   ├── *.py
│   │   └── __init__.py
│   └── skills/                     # Reusable skills
│       ├── *.py
│       └── __init__.py
├── CLAUDE.md                       # Root navigation
├── README.md
└── .env.example
```

### CLAUDE.md Hierarchy

**Root CLAUDE.md** (`phase2/CLAUDE.md`)
```markdown
# Phase II – Implementation Guidelines

## Quick Navigation
- Frontend development: See `/frontend/CLAUDE.md`
- Backend development: See `/backend/CLAUDE.md`
- Specification: See `/specs/001-fullstack-web-app/spec.md`
- Planning: See `/specs/001-fullstack-web-app/plan.md`

## Workflow
1. Read specification
2. Review architecture plan
3. Implement feature following layer-specific guidelines
4. Reference agents & skills in /src
```

**Frontend CLAUDE.md** (`phase2/frontend/CLAUDE.md`)
```markdown
# Frontend Development Guidelines

## Rules
- All user actions communicate via REST API only
- JWT token attached to every API request via Authorization header
- Protected routes check for JWT before rendering
- Error messages are user-friendly, never expose technical details

## API Client Usage
Import from `@/utils/api-client`:
```typescript
const response = await apiClient.post(`/api/users/${userId}/tasks`, body);
```

## Protected Routes Pattern
Wrap in AuthGuard component which:
- Checks for JWT token
- Redirects to login if missing/expired
- Shows loading state while checking auth
```

**Backend CLAUDE.md** (`phase2/backend/CLAUDE.md`)
```markdown
# Backend Development Guidelines

## Rules
- Every endpoint requires valid JWT token
- URL {user_id} MUST match authenticated user_id
- All database queries filtered by user_id
- Return standardized error responses

## JWT Middleware
Applied to all routes:
- Validates JWT signature
- Extracts user_id from claims
- Validates URL user_id == JWT user_id
- Sets request.user_id for handlers

## Service Layer Pattern
Business logic isolated in services/:
```python
async def create_task(user_id: str, title: str, description: str):
    # All queries scoped to user_id
    return await task_service.create(user_id, title, description)
```
```

### Spec References with @specs Paths

Throughout implementation, reference specs:
```
@specs/001-fullstack-web-app/spec.md (REQ-API-001)
@specs/001-fullstack-web-app/spec.md (User Story 1)
@specs/001-fullstack-web-app/plan.md (Architecture Sketch)
```

---

## 3. Planning & Research Approach

### Research-Concurrent Workflow

**Phase 0A: Research (Parallel Tasks)**

| Task | Duration | Outcome |
|------|----------|---------|
| Better Auth + JWT patterns | Concurrent | research.md section: Authentication |
| Neon PostgreSQL + SQLModel setup | Concurrent | research.md section: Database |
| Next.js 16+ App Router patterns | Concurrent | research.md section: Frontend Arch |
| FastAPI + Pydantic validation | Concurrent | research.md section: Backend Arch |

**Phase 0B: Spec Refinement**
- Based on research findings, update specs
- Document any technology-specific adjustments
- Validate compatibility between layers

**Phase 1: Design** (Dependent on research)
- Generate data-model.md from entity specs
- Create API contracts from functional requirements
- Define error handling conventions
- Update agent context with technology choices

**Phase 2: Implementation** (Dependent on design)
- Generate frontend code via Claude Code
- Generate backend code via Claude Code
- Generate database migrations via Claude Code
- Validate against specs using agents

### Agents Used During Planning

| Agent | When | Purpose |
|-------|------|---------|
| **SpecificationInterpreterAgent** | Phase 0B | Parse specs, detect inconsistencies |
| **APIDesignValidationAgent** | Phase 1 | Validate API contract against JWT & user_id rules |
| **AuthenticationReasoningAgent** | Phase 0A | Reason about JWT flow, identify risks |
| **FrontendArchitectureAgent** | Phase 1 | Map specs to pages/components |
| **BackendArchitectureAgent** | Phase 1 | Validate service layer, query patterns |
| **IntegrationConsistencyAgent** | Phase 1 | Detect field mismatches, scope drift |

---

## 4. Key Decisions & Documentation

### Decision 1: Monorepo vs Separate Repositories

| Option | Pros | Cons | Selected |
|--------|------|------|----------|
| **Monorepo** | Single version control, easier coordination, shared specs | Larger repo, potential merge conflicts | ✅ YES |
| **Separate** | Independent scaling, isolated concerns | Harder to keep specs in sync, version management | ❌ |

**Rationale**: Phase II requires tight integration between frontend and backend. Monorepo enables shared specification and coordinated changes.

**Tradeoffs**: Accept larger repository size for better coordination.

---

### Decision 2: JWT Verification Strategy in FastAPI

| Option | Approach | Pros | Cons | Selected |
|--------|----------|------|------|----------|
| **Middleware** | Global middleware validates all requests | Centralized, consistent | Can't customize per-route | ✅ YES |
| **Dependency** | Per-route injection validates | Fine-grained control | Duplicate code on many routes | ❌ |

**Rationale**: Middleware ensures all endpoints are protected without per-route boilerplate.

**Implementation**: Custom JWT middleware in `backend/src/middleware/auth.py` validates token and injects user_id into request context.

---

### Decision 3: User ID in URL vs JWT Only

| Option | Approach | Pros | Cons | Selected |
|--------|----------|------|------|----------|
| **Both (URL + JWT)** | `/api/users/{user_id}/tasks` with JWT verification | Explicit in URL, matches spec, enforces ownership | Requires two checks | ✅ YES |
| **JWT Only** | `/api/tasks` with user_id from JWT | Simpler URLs | Less explicit, harder to debug | ❌ |

**Rationale**: Specification explicitly requires user_id in URL for clarity and debugging. JWT verification ensures security.

**Implementation**: Middleware validates URL user_id == JWT user_id, returns 403 if mismatch.

---

### Decision 4: SQLModel Relationship Modeling

| Option | Approach | Pros | Cons | Selected |
|--------|----------|------|------|----------|
| **Foreign Key** | `tasks.user_id` links to `users.id` | Referential integrity, database enforces | Requires user existence | ✅ YES |
| **No Relationship** | Manual user_id in task | Simpler schema | No integrity guarantee | ❌ |

**Rationale**: Specification requires data integrity and multi-user support.

**Implementation**: SQLModel defines explicit foreign key with cascade rules.

---

### Decision 5: Frontend Data-Fetching Strategy

| Option | Approach | Pros | Cons | Selected |
|--------|----------|------|------|----------|
| **Client Components** | All data fetched in useEffect | Dynamic, real-time updates | More client-side complexity | ✅ YES |
| **Server Components** | Server-side rendering | Better SEO, less JS sent | Harder to implement auth checks | ❌ |

**Rationale**: Authentication requires client-side state checking. Client components simpler for dashboard.

**Implementation**: Protected layout checks JWT, wrapped TaskList fetches via useEffect hook.

---

### Decision 6: Error Handling & HTTP Status Conventions

| Status | Meaning | Use Case |
|--------|---------|----------|
| **400** | Bad Request | Title empty, invalid input |
| **401** | Unauthorized | Missing JWT, expired token |
| **403** | Forbidden | User ID mismatch, cross-user access |
| **404** | Not Found | Task doesn't exist |
| **500** | Server Error | Database connection failed |

**Rationale**: Align with REST standards and spec requirements.

**Implementation**: Error normalization skill converts exceptions to appropriate HTTP status.

---

## 5. Reusable Intelligence Integration Plan

### Agents During Implementation

**APIDesignValidationAgent** validates each route:
```python
# During backend development
agent = APIDesignValidationAgent()
endpoint = {
    "path": "/api/{user_id}/tasks",
    "method": "POST",
    "headers": {"Authorization": "Bearer <token>"},
}
assert agent.validate_jwt_enforcement(endpoint)
assert agent.validate_user_id_matching(endpoint)
```

**AuthenticationReasoningAgent** guides JWT implementation:
```python
# During auth middleware development
agent = AuthenticationReasoningAgent()
jwt_rules = agent.define_jwt_verification_logic()
# Follow rules for: signature validation, expiry check, user_id extraction
```

**DataOwnershipEnforcementAgent** ensures query safety:
```python
# During service layer development
agent = DataOwnershipEnforcementAgent()
rules = agent.generate_filtered_query_rules(user_id, "list_tasks")
# Apply WHERE clause: WHERE user_id = ? in all queries
```

### Skills Reused Across Layers

**JWT Validation Skill** (Used in: Backend Middleware)
```python
from src.skills import JWTValidationSkill

jwt_skill = JWTValidationSkill()
result = jwt_skill.validate_jwt(token)
# Returns: {is_valid, user_id, token_expiry}
```

**Authorization Matching Skill** (Used in: Backend Routes)
```python
from src.skills import AuthorizationMatchingSkill

auth_skill = AuthorizationMatchingSkill()
is_authorized = auth_skill.is_authorized(token_user_id, url_user_id)
# Returns: boolean
```

**Frontend API Client Skill** (Used in: Frontend Utils)
```typescript
// TypeScript translation of frontend_api_client_skill.py
import { FrontendAPIClientSkill } from '@/src/skills';

const apiClient = new FrontendAPIClientSkill();
const authorizedRequest = apiClient.build_authorized_request(
  "POST",
  "/api/users/123/tasks",
  jwtToken,
  {title: "Buy milk"}
);
```

**Error Normalization Skill** (Used in: Frontend & Backend)
```python
# Backend
from src.skills import ErrorNormalizationSkill

error_skill = ErrorNormalizationSkill()
safe_response = error_skill.normalize_error({"type": "jwt_expired"})
# Returns: {user_safe_message, http_status_code}

# Frontend - translate error responses using same logic
```

**API Intent Mapping Skill** (Used in: Frontend API Client)
```typescript
// Frontend routes user action to API endpoint
import { APIIntentMappingSkill } from '@/src/skills';

const intentSkill = new APIIntentMappingSkill();
const endpoint = intentSkill.map_intent_to_endpoint("create");
// Returns: {http_method: "POST", endpoint_pattern: "/api/{user_id}/tasks"}
```

### No Code Duplication

- Validation logic lives in **Skills**, not in route handlers
- Auth reasoning lives in **Agents**, not in route code
- Error messages generated from **Skills**, not hardcoded
- Query patterns enforced via **Agents**, checked in code review

---

## 6. Testing & Quality Validation Strategy

### Backend Validation (No Manual Test Framework)

**Requirement**: Unauthorized requests return 401
```
Input: API call without Authorization header
Expected: 401 Unauthorized response
Validation: Check response status code == 401
```

**Requirement**: JWT-required enforcement on all endpoints
```
Input: Enumerate all routes in routes/tasks.py
Expected: Each route has @require_jwt decorator
Validation: Agent scans code, verifies decorator presence
```

**Requirement**: User cannot access another user's tasks
```
Input: User A's JWT, request /api/users/user-b-id/tasks
Expected: 403 Forbidden (user_id mismatch)
Validation: Middleware validates user_id == JWT user_id
```

### Frontend Validation

**Requirement**: Authenticated UI rendering
```
Input: User not logged in (no JWT)
Expected: Redirect to login page
Validation: AuthGuard component checks localStorage for token
```

**Requirement**: Task CRUD behavior
```
Input: User creates task "Buy milk"
Expected: Task appears in list immediately
Validation: Component state updates after API success
```

**Requirement**: Error handling
```
Input: API returns 401 (expired token)
Expected: User redirected to login
Validation: API client intercepts 401, redirects
```

### Integration Validation

**Requirement**: JWT flow end-to-end
```
Steps:
1. User signs up with Better Auth → JWT issued
2. Frontend stores JWT in localStorage
3. Frontend makes API call, attaches JWT in Authorization header
4. Backend validates JWT signature, extracts user_id
5. Route handler executes, returns data
Expected: Task created and stored in database
Validation: Check database for task with correct user_id
```

**Requirement**: Data persistence across sessions
```
Steps:
1. User creates task
2. User logs out
3. User logs in again
4. User views task list
Expected: Previously created task visible
Validation: Task retrieved from database, same data as before
```

---

## 7. Phase Organization

### Phase A: Research

**Tasks**:
1. Better Auth + JWT implementation patterns
2. Neon PostgreSQL + SQLModel usage
3. Next.js 16+ App Router advanced patterns
4. FastAPI security best practices
5. PostgreSQL schema optimization

**Output**: `research.md` with all findings

**Duration**: Concurrent execution

---

### Phase B: Foundation

**Tasks**:
1. Create spec-kit configuration (if needed)
2. Setup CLAUDE.md hierarchy (root, frontend, backend)
3. Create base project structure
4. Create environment example (.env.example)
5. Document build/run commands

**Output**:
- `phase2/CLAUDE.md`
- `phase2/frontend/CLAUDE.md`
- `phase2/backend/CLAUDE.md`
- `phase2/.env.example`

**Depends on**: Phase A

---

### Phase C: Analysis & Design

**Tasks**:
1. Parse specs using SpecificationInterpreterAgent
2. Generate `data-model.md` from entities
3. Generate API contracts in `contracts/`
4. Validate contracts using APIDesignValidationAgent
5. Update agent context with technology choices

**Output**:
- `specs/001-fullstack-web-app/data-model.md`
- `specs/001-fullstack-web-app/contracts/tasks-endpoints.md`
- `specs/001-fullstack-web-app/contracts/auth-flow.md`
- Updated agent context

**Depends on**: Phase B

---

### Phase D: Synthesis & Implementation

**Tasks**:
1. Generate frontend code (pages, components, hooks, utils)
2. Generate backend code (routes, models, services, middleware)
3. Generate database migrations
4. Generate test/validation code
5. Validate against specs using agents

**Output**:
- Complete Next.js frontend application
- Complete FastAPI backend application
- Database schema and migrations
- Test suite

**Depends on**: Phase C

---

### Phase E: Validation & Documentation

**Tasks**:
1. Run validation scenarios from Section 6
2. Create integration tests
3. Document deployment process
4. Update README with setup instructions
5. Create PHR documenting implementation

**Output**:
- Validation results
- Deployment guide
- Updated README
- PHR file

**Depends on**: Phase D

---

## Execution Summary

| Phase | Duration | Agents Used | Output |
|-------|----------|-------------|--------|
| **A: Research** | Concurrent | AuthenticationReasoningAgent, Frontend/Backend ArchitectureAgents | research.md |
| **B: Foundation** | Sequential | None | CLAUDE.md hierarchy + env setup |
| **C: Analysis** | Sequential | SpecificationInterpreterAgent, APIDesignValidationAgent, IntegrationConsistencyAgent | data-model.md, contracts/ |
| **D: Synthesis** | Sequential | All agents as validators | Frontend + Backend code |
| **E: Validation** | Sequential | IntegrationConsistencyAgent | Validation results + PHR |

---

## Next Steps

1. ✅ Research Phase (Phase A) - Begin concurrent research tasks
2. ⬜ Foundation Phase (Phase B) - Setup Spec-Kit and CLAUDE.md files
3. ⬜ Analysis Phase (Phase C) - Generate design artifacts
4. ⬜ Synthesis Phase (Phase D) - Generate implementation code
5. ⬜ Validation Phase (Phase E) - Validate and document

---

**Plan Status**: Ready for Phase A (Research)
**Plan Location**: `phase2/specs/001-fullstack-web-app/plan.md`
**Associated Spec**: `phase2/specs/001-fullstack-web-app/spec.md`
**Agents Location**: `phase2/src/agents/`
**Skills Location**: `phase2/src/skills/`
