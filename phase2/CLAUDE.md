# CLAUDE.md – Phase II Development Guide

**Project**: Hackathon II – The Evolution of Todo – Phase II Full-Stack Web Application
**Repository**: phase2/
**Status**: Implementation Ready
**Model**: Claude Haiku 4.5
**Date**: January 4, 2026

---

## Quick Navigation

### Specifications (Start Here)
- **Overview**: `specs/overview.md` – System vision, architecture, tech stack
- **Feature Specs**:
  - `specs/features/authentication.md` – JWT, user signup/login
  - `specs/features/task-crud.md` – Task CRUD operations, data model
- **API Contract**: `specs/api/rest-endpoints.md` – Complete endpoint specifications
- **Database Schema**: `specs/database/schema.md` – SQLModel definitions, query patterns

### Planning & Breakdown
- **Implementation Plan**: `specs/001-fullstack-web-app/plan.md` – Architecture, decisions, phases
- **Task Breakdown**: `specs/001-fullstack-web-app/tasks.md` – 35 tasks, dependencies, parallelization

### Development
- **Frontend Guide**: `frontend/CLAUDE.md` – Next.js patterns, API client, protected routes
- **Backend Guide**: `backend/CLAUDE.md` – FastAPI patterns, JWT middleware, services
- **Agents**: `src/agents/` – Reasoning agents for specification validation
- **Skills**: `src/skills/` – Reusable logic components

### Documentation History
- **Specification PHR**: `docs-history/prompts/001-phase-ii-specification-request.phr.md`
- **Planning PHR**: `docs-history/prompts/002-phase-ii-implementation-plan.phr.md`
- **Task Breakdown PHR**: `docs-history/prompts/003-phase-ii-task-breakdown.phr.md`

---

## Project Structure

```
phase2/
├── frontend/                          # Next.js 16+ application
│   ├── CLAUDE.md                      # Frontend development rules
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── src/
│   │   ├── app/                       # App Router pages
│   │   │   ├── auth/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── signup/page.tsx
│   │   │   └── dashboard/
│   │   │       ├── page.tsx
│   │   │       └── layout.tsx
│   │   ├── components/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskForm.tsxn
│   │   │   └── AuthGuard.tsx
│   │   └── utils/
│   │       ├── api-client.ts          # Fetch wrapper with JWT
│   │       └── auth.ts                # Token storage/retrieval
│   └── .env.example
│
├── backend/                           # FastAPI application
│   ├── CLAUDE.md                      # Backend development rules
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── main.py                        # FastAPI app entry
│   └── src/
│       ├── config.py                  # Config loading
│       ├── db/
│       │   ├── database.py            # DB connection
│       │   └── models.py              # SQLModel definitions
│       ├── models/
│       │   ├── user.py                # User model
│       │   └── task.py                # Task model
│       ├── schemas/
│       │   ├── user.py                # Pydantic schemas
│       │   └── task.py
│       ├── middleware/
│       │   └── auth.py                # JWT validation
│       ├── services/
│       │   └── task_service.py        # Business logic
│       └── api/
│           └── routes/
│               ├── auth.py            # Auth endpoints
│               └── tasks.py           # Task CRUD endpoints
│   └── .env.example
│
├── src/
│   ├── agents/                        # Reasoning agents (validation, analysis)
│   │   ├── __init__.py
│   │   ├── specification_interpreter_agent.py
│   │   ├── api_design_validation_agent.py
│   │   ├── authentication_reasoning_agent.py
│   │   ├── frontend_architecture_agent.py
│   │   ├── backend_architecture_agent.py
│   │   └── integration_consistency_agent.py
│   │
│   └── skills/                        # Reusable stateless logic
│       ├── __init__.py
│       ├── jwt_validation_skill.py
│       ├── authorization_matching_skill.py
│       ├── api_intent_mapping_skill.py
│       ├── data_ownership_enforcement_skill.py
│       ├── error_normalization_skill.py
│       ├── frontend_api_client_skill.py
│       └── spec_traceability_skill.py
│
├── specs/
│   ├── overview.md                    # System vision
│   ├── features/
│   │   ├── authentication.md          # Auth feature spec
│   │   └── task-crud.md               # Task CRUD feature spec
│   ├── api/
│   │   └── rest-endpoints.md          # API contract
│   ├── database/
│   │   └── schema.md                  # DB schema & queries
│   └── 001-fullstack-web-app/
│       ├── spec.md                    # Complete specification
│       ├── plan.md                    # Implementation plan
│       └── tasks.md                   # Task breakdown (35 tasks)
│
├── docs-history/
│   └── prompts/
│       ├── 001-phase-ii-specification-request.phr.md
│       ├── 002-phase-ii-implementation-plan.phr.md
│       └── 003-phase-ii-task-breakdown.phr.md
│
└── README.md                          # Setup & deployment guide
```

---

## Core Principles

### 1. Spec-Driven Development
- **All code generation follows specifications**
- Specifications are authoritative sources of truth
- Changes to requirements update specs first, then code
- No features implemented outside specifications

### 2. Phase Separation
- Phase II is completely independent from Phase I
- No shared code, no imports from phase1/
- Each phase has its own frontend/, backend/, src/ directories
- Phases can be run independently

### 3. Multi-User Isolation
- **Every API request scoped to authenticated user**
- Database queries always include `WHERE user_id = ?`
- URL `user_id` verified against JWT `user_id`
- Cross-user access returns 403 Forbidden

### 4. JWT Security
- **All endpoints (except signup/login) require Authorization header**
- JWT token contains user_id, expiration, issued-at
- Signature verified on every request
- Expired/invalid tokens return 401 Unauthorized

### 5. REST API Conventions
- Standard HTTP methods: POST (create), GET (read), PUT (update), DELETE (delete), PATCH (partial)
- Standard status codes: 200, 201, 204, 400, 401, 403, 404, 500
- JSON request/response bodies
- Consistent error response format

### 6. No Hardcoded Secrets
- All secrets in environment variables (.env)
- JWT_SECRET, DATABASE_URL, BETTER_AUTH_SECRET never in code
- .env.example shows all required variables
- .gitignore excludes .env files

### 7. Reusable Intelligence
- Agents: Validate specifications, detect inconsistencies, reason about requirements
- Skills: Stateless, reusable logic across layers (JWT validation, API client, error handling)
- No code duplication across frontend/backend/middleware

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | Next.js | 16+ |
| Frontend | React | 19+ |
| Frontend | TypeScript | 5.0+ |
| Backend | FastAPI | 0.110+ |
| Backend | Python | 3.10+ |
| Backend | SQLModel | 0.0.14+ |
| Database | PostgreSQL | 15+ (Neon) |
| Auth | Better Auth | Latest |
| Auth | PyJWT | 2.8+ |

---

## Implementation Phases

### Phase 1: Setup & Project Initialization (3 tasks)
- Create project directories
- Initialize frontend package.json
- Initialize backend requirements.txt

### Phase 2: Foundation & Infrastructure (7 tasks)
- Environment configuration
- Database connection
- SQLModel definitions
- JWT middleware
- Frontend token storage
- Frontend API client

### Phase 3: User Story 1 – User Registration & First Task (8 tasks)
- User & Task models
- Pydantic schemas
- Task service (create)
- Signup & login pages
- POST /api/{user_id}/tasks endpoint

### Phase 4: User Story 2 – Task CRUD Operations (9 tasks)
- GET, PUT, DELETE, PATCH endpoints
- Task service methods (list, get, update, delete, toggle)
- TaskList & TaskForm components
- Dashboard page

### Phase 5: User Story 3-4 – Multi-User Isolation & JWT Security (5 tasks)
- Authorization validation (user_id matching)
- Query filtering in services
- AuthGuard component
- Protected dashboard layout
- Error handling (401/403)

### Phase 6: Validation & Polish (3 tasks)
- End-to-end JWT flow validation
- Data persistence validation
- README documentation

**Total: 35 tasks**

---

## Agents & Skills Usage

### During Implementation

**Agents** (use before code generation to validate):
1. **SpecificationInterpreter**: Parse specs, extract requirements, detect conflicts
2. **APIDesignValidation**: Validate endpoints, JWT enforcement, user_id matching
3. **AuthenticationReasoning**: JWT flow reasoning, verification logic
4. **FrontendArchitecture**: Map specs to pages/components
5. **BackendArchitecture**: Validate model-schema alignment
6. **IntegrationConsistency**: Detect field mismatches, naming consistency

**Skills** (use during implementation for reusable logic):
1. **JWTValidationSkill**: Token parsing, expiration checking
2. **AuthorizationMatchingSkill**: URL user_id vs JWT user_id
3. **APIIntentMapping**: CRUD operation to REST endpoint
4. **DataOwnershipEnforcement**: Generate user-filtered queries
5. **ErrorNormalization**: Convert errors to safe messages
6. **FrontendAPIClient**: Attach JWT to requests
7. **SpecTraceability**: Trace decisions back to specs

### Example: Implementing Task Service

1. **Validate with BackendArchitecture agent**: Check service signatures match API contracts
2. **Use DataOwnershipEnforcement skill**: Generate `WHERE user_id = ?` queries
3. **Use ErrorNormalization skill**: Format error responses
4. **Reference SpecTraceability skill**: Trace to task-crud.md REQ-TASK-001

---

## Key Files to Know

### Specifications (Always Reference)
- `specs/001-fullstack-web-app/spec.md` – User stories, requirements, success criteria
- `specs/api/rest-endpoints.md` – Complete API contracts with examples
- `specs/database/schema.md` – Query patterns, Pydantic schemas

### Implementation Guides
- `frontend/CLAUDE.md` – Patterns, rules, conventions for frontend code
- `backend/CLAUDE.md` – Patterns, rules, conventions for backend code

### Task Tracking
- `specs/001-fullstack-web-app/tasks.md` – All 35 tasks with dependencies

---

## Common Implementation Patterns

### Backend: Task Service with User Isolation

```python
# backend/src/services/task_service.py
def get_user_tasks(session: Session, user_id: str, status: Optional[str] = None):
    # Always filter by user_id for isolation
    query = session.query(Task).filter(Task.user_id == user_id)

    if status:
        query = query.filter(Task.status == status)

    return query.order_by(Task.created_at.desc()).all()
```

### Backend: API Endpoint with JWT Verification

```python
# backend/src/api/routes/tasks.py
@router.get("/api/users/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    request: Request,
    session: Session = Depends(get_session)
):
    # Middleware already verified JWT and user_id match
    # request.state.user_id contains authenticated user
    tasks = task_service.get_user_tasks(session, user_id)
    return {"success": True, "data": tasks}
```

### Frontend: API Client with JWT Attachment

```typescript
// frontend/src/utils/api-client.ts
export async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getToken(); // From localStorage or cookie

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`/api${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) throw new Error(response.statusText);
  return response.json();
}
```

### Frontend: Protected Route with AuthGuard

```typescript
// frontend/src/components/AuthGuard.tsx
export function AuthGuard({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/auth/login");
    } else {
      setIsAuthenticated(true);
    }
  }, []);

  if (!isAuthenticated) return null;
  return children;
}
```

---

## Error Handling Standards

### Backend Error Response Format

```python
{
  "success": False,
  "error": "error_code",
  "message": "User-friendly message"
}
```

### HTTP Status Codes
- `200 OK` – Successful GET/PUT/PATCH
- `201 Created` – Successful POST
- `204 No Content` – Successful DELETE
- `400 Bad Request` – Validation error
- `401 Unauthorized` – Missing/invalid JWT
- `403 Forbidden` – User ID mismatch
- `404 Not Found` – Resource doesn't exist
- `500 Server Error` – Unrecoverable error

### Frontend Error Handling

```typescript
try {
  const data = await apiCall("/api/users/{userId}/tasks");
} catch (error) {
  if (error.status === 401) {
    // Redirect to login
    router.push("/auth/login");
  } else if (error.status === 403) {
    // Show access denied
    toast.error("You don't have permission");
  } else {
    // Show generic error
    toast.error("Something went wrong");
  }
}
```

---

## Security Checklist

Before implementation completion, verify:

- [ ] All endpoints require `Authorization: Bearer <token>`
- [ ] JWT signature verified on every request
- [ ] JWT expiration checked
- [ ] `user_id` from URL matches JWT `sub`
- [ ] All queries include `WHERE user_id = ?`
- [ ] No hardcoded secrets in code
- [ ] Error messages don't leak sensitive info
- [ ] Cross-user access returns 403
- [ ] Missing JWT returns 401
- [ ] `.env` files in `.gitignore`

---

## Development Workflow

### 1. Read Specifications First
Always start by reading the relevant specification:
- `specs/overview.md` for system understanding
- `specs/api/rest-endpoints.md` for API details
- `specs/database/schema.md` for data structures
- Feature specs for specific requirements

### 2. Validate with Agents
Before implementing, use agents to validate:
- Spec consistency and completeness
- API design alignment
- Database schema correctness

### 3. Implement with Skills
Reuse skills for common patterns:
- JWT validation across endpoints
- User filtering across queries
- Error handling across layers

### 4. Reference Tasks
Use `tasks.md` to track progress:
- Task IDs (T001-T035)
- Dependencies between tasks
- Parallelization opportunities

### 5. Test Independent Criteria
Verify independent test criteria from `tasks.md`:
- US1: Signup, JWT, first task
- US2: Full CRUD operations
- US3: Multi-user isolation
- US4: JWT security

---

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host/dbname
JWT_SECRET=your-secret-key-here
BETTER_AUTH_SECRET=your-better-auth-secret
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Getting Help

### If You Need to Understand:
- **What to build**: See `specs/001-fullstack-web-app/spec.md`
- **How to build**: See `plan.md` and feature specs
- **Which task to do**: See `tasks.md`
- **How to code it**: See `frontend/CLAUDE.md` or `backend/CLAUDE.md`

### If Code Generation Issues:
- Check agents in `src/agents/` for validation
- Use skills in `src/skills/` for reusable patterns
- Reference PHR files in `docs-history/prompts/` for decision history

---

## Success Criteria

Phase II implementation is complete when:

1. ✅ User can signup with email/password
2. ✅ User receives JWT token
3. ✅ User can login with credentials
4. ✅ User can create tasks via API
5. ✅ User can read their tasks (list & single)
6. ✅ User can update tasks
7. ✅ User can delete tasks
8. ✅ User can toggle task completion
9. ✅ User can only see/modify their own tasks
10. ✅ All endpoints require valid JWT
11. ✅ Data persists in PostgreSQL
12. ✅ No hardcoded secrets

---

**Last Updated**: January 4, 2026
**Status**: Ready for Implementation via `/sp.implement`
