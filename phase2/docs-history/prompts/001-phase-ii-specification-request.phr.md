# PHR: Phase II Full-Stack Web App Specification Request

**Timestamp**: January 4, 2026
**Model**: Claude Haiku 4.5
**Task Type**: Specification & Documentation
**Stage**: Spec

---

## PROMPT_TEXT

```
Phase: Phase II – Todo Full-Stack Web Application
Project: Hackathon II – The Evolution of Todo (Spec-Driven Development)

Objective:
Specify the requirements for transforming the Phase I in-memory
console Todo application into a full-stack, multi-user web application
with persistent storage, authentication, and a RESTful API.
All development must follow Spec-Driven Development using
Claude Code and Spec-Kit Plus. No manual coding is allowed.

Target Audience:
- Hackathon II judges evaluating full-stack, AI-native development
- Developers implementing the specification using Claude Code

Core Requirements:

DATABASE & PERSISTENCE:
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Task data must persist across sessions
- Database schema must include:
  - users table (managed by Better Auth)
  - tasks table linked to users by user_id

AUTHENTICATION & SECURITY:
- JWT token issued by Better Auth
- Token passed via Authorization header
- Backend verifies JWT signature using shared secret
- user_id in URL must match authenticated user_id
- Unauthorized requests return HTTP 401
- Cross-user data access is strictly forbidden

ARCHITECTURE & STRUCTURE:
- Monorepo with /frontend (Next.js) and /backend (FastAPI)
- /specs directory for Spec-Kit organized documentation
- Multiple CLAUDE.md files (root, frontend-specific, backend-specific)
- Specs referenced using @specs/... notation

FRONTEND TECHNOLOGY:
- Next.js 16+ (App Router)
- TypeScript
- Responsive design
- 5 core features via web UI: add, list, update, delete, mark complete

BACKEND TECHNOLOGY:
- Python FastAPI
- SQLModel ORM with Neon PostgreSQL
- RESTful API endpoints for all 5 features
- JWT authentication on every endpoint

SUCCESS CRITERIA:
- All five basic Todo features work via web UI
- All API endpoints function correctly
- JWT authentication enforced on every request
- Users can only see and modify their own tasks
- Data persists in Neon PostgreSQL
- Frontend and backend integrated correctly
- No manual code changes required

CONSTRAINTS:
- No console-only interaction (web-only)
- No in-memory storage (persistent only)
- No manual coding (100% AI-generated)
- No bypassing authentication
- No hardcoded secrets
- No AI chatbot in this phase

OUT OF SCOPE:
- Chatbot or natural language interface
- Background jobs or queues
- Role-based access control
- Offline support
- Mobile-native apps
- Analytics or reporting dashboards

DELIVERABLES:
- Structured specs under /specs directory
- API specification with all endpoints
- Database schema specification
- UI component/page specifications
- Authentication flow specification
- Ready for next step: `/sp.plan`
```

---

## RESPONSE_TEXT

### What Was Created

**1. Phase II Folder Structure**
- Created `/phase2/` directory completely separate from Phase I
- Organized into: `/frontend`, `/backend`, `/specs`, `/docs-history`, `/docs`
- Ensures no code mixing between Phase I and Phase II

**2. Specification Document**
- Location: `phase2/specs/001-fullstack-web-app/spec.md`
- Comprehensive specification document covering:
  - Executive summary and objectives
  - Complete scope definition (in/out of scope)
  - 5 detailed user scenarios with workflows
  - 30+ functional requirements organized by category:
    - Authentication & Security (5 reqs)
    - Task Management CRUD (5 reqs)
    - Data Persistence (3 reqs)
    - API Response Format (3 reqs)
    - Frontend UI (6 reqs)
    - Environment & Configuration (2 reqs)
  - 17 measurable success criteria
  - Complete data model (User, Task entities with fields)
  - API endpoint specifications with request/response examples
  - 3-tier architecture diagram and integration points
  - 10 documented assumptions
  - 22 test scenarios (unit, integration, security)
  - 5+ edge case scenarios

**3. Documentation Structure**
- Created `phase2/docs-history/prompts/` folder for PHRs
- Ready for plan, tasks, and implementation PHRs

### Key Decisions Made

**1. Architecture**: 3-tier web application
   - Frontend: Next.js with TypeScript
   - Backend: FastAPI with SQLModel
   - Database: Neon PostgreSQL

**2. Authentication**: JWT-based with Better Auth
   - Tokens include user_id
   - Every API request validated
   - Cross-user access prevented

**3. Data Model**:
   - users table (Better Auth managed)
   - tasks table with user_id foreign key
   - Status enum: "incomplete" | "complete"

**4. API Design**: REST with standardized responses
   - Endpoints: POST, GET, PUT, DELETE, PATCH
   - All user-scoped: `/api/users/{user_id}/tasks`
   - JSON request/response format
   - HTTP status codes: 200, 201, 204, 400, 401, 403, 404, 500

**5. Security**:
   - JWT signature verification on backend
   - URL user_id must match authenticated user_id
   - Cross-user access returns 403 Forbidden
   - No hardcoded secrets (environment variables)

### Requirements Captured

**From Your Input**:
- ✅ Full-stack transformation from console to web
- ✅ Multi-user with persistent storage
- ✅ All 5 core features (add, list, update, delete, toggle)
- ✅ JWT authentication on every endpoint
- ✅ SQLModel ORM with Neon PostgreSQL
- ✅ Next.js 16+ with App Router
- ✅ Responsive design
- ✅ User data isolation
- ✅ No manual coding (AI-native)
- ✅ Spec-Driven Development approach

### Scope Boundaries

**In Scope** (explicitly covered):
- Web UI (not console)
- Persistent storage (not in-memory)
- Multi-user with authentication
- REST API endpoints
- JWT validation
- Responsive design

**Out of Scope** (explicitly excluded):
- Chatbot/NLP
- Background jobs/queues
- Role-based access control
- Offline support
- Mobile-native apps
- Analytics dashboards

### Success Metrics Defined

**Functional**:
- 5 core features working via web UI
- API endpoints function correctly
- JWT enforced on all requests
- User isolation working
- Data persists in PostgreSQL

**Security**:
- No cross-user access possible
- No hardcoded secrets
- Token validation on every request
- user_id verification in paths

**Quality**:
- 100% AI-generated code
- Spec sufficient for implementation
- All requirements testable

---

## What This Enables

### For Planning Phase
Specification provides clear requirements for:
- Frontend architecture and component design
- Backend service structure and endpoints
- Database schema and ORM models
- Test cases and validation

### For Implementation Phase
Developers (or Claude Code) can:
- Generate Next.js components and pages
- Create FastAPI routes and middleware
- Define SQLModel database models
- Write comprehensive tests
- Implement JWT validation logic

### For Quality Assurance
QA team can:
- Test all 22 test scenarios
- Verify success criteria
- Validate edge cases
- Confirm user isolation
- Check API contracts

---

## Next Steps

1. **Planning** (`/sp.plan`): Create implementation plan from specification
2. **Task Breakdown** (`/sp.tasks`): Generate TDD task list
3. **Implementation** (`/sp.implement`): Generate production code
4. **Testing**: Verify all success criteria met

---

## Artifacts Created

```
phase2/
├── specs/
│   └── 001-fullstack-web-app/
│       └── spec.md                 ← Complete specification document
├── docs-history/
│   └── prompts/
│       └── 001-phase-ii-specification-request.phr.md  ← This PHR
└── folder structure initialized
```

---

**Status**: ✅ SPECIFICATION DOCUMENTED
**Ready for**: `/sp.plan` (Planning Phase)
**Date**: January 4, 2026
