# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `001-ai-todo-chatbot` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-ai-todo-chatbot/spec.md`

## Summary

Implement a conversational AI-powered todo chatbot that allows users to manage tasks through natural language. The system uses OpenAI Agents SDK for intent understanding and reasoning, MCP (Model Context Protocol) tools for deterministic task operations, and maintains a stateless, cloud-native architecture with conversation persistence in Neon PostgreSQL.

**Core Value**: Enable natural language task management (add, view, update, complete, delete) through a chat interface without forms or buttons, with full conversation context persistence and strict user isolation.

**Technical Approach**: Single stateless POST endpoint receives chat messages, reconstructs conversation context from database, executes OpenAI Agent with MCP tool access, persists new conversation turn, and returns agent response.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.104+, OpenAI Agents SDK (latest), MCP SDK (official), SQLModel 0.0.14+, Better Auth (JWT), OpenAI ChatKit (frontend)
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest with pytest-asyncio, httpx for API testing
**Target Platform**: Cloud-native (Vercel/Render for deployment)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <3s response time for 95% requests, support 100 concurrent users
**Constraints**: Stateless backend (zero in-memory conversation state), MCP-exclusive task operations, JWT on every request
**Scale/Scope**: MVP with 5 CRUD operations, ~100-1000 users expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| I. Deterministic AI Behavior | All agent actions must map to explicit MCP tool calls | ✅ PASS - Agent uses only MCP tools (add_task, list_tasks, update_task, complete_task, delete_task) |
| II. Spec-Driven Reproducibility | All behaviors documented in specifications | ✅ PASS - 15 functional requirements in spec.md cover all behaviors |
| III. Stateless, Cloud-Native Architecture | Zero in-memory conversation state | ✅ PASS - Conversation reconstructed from DB on every request |
| IV. Separation of Concerns | Clear UI → Agent → MCP → DB boundaries | ✅ PASS - ChatKit UI, Agent reasoning, MCP tools, DB persistence separated |
| V. Security-First Design | JWT auth + user isolation on every request | ✅ PASS - JWT required, user_id matching enforced, queries filtered by user_id |
| VI. Graceful Error Handling | User-friendly error messages | ✅ PASS - Spec requires no stack traces, agent confirms actions |

**Tooling Standards Check**:
- ✅ Required MCP tools defined: add_task, list_tasks, update_task, complete_task, delete_task
- ✅ All tools accept user_id for isolation
- ✅ Tools return structured responses with human-readable messages
- ✅ Agent confirms task mutations

**Architecture Rules Check**:
- ✅ Single stateless endpoint: POST /api/{user_id}/chat
- ✅ Technology stack enforced: FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL, Better Auth

**Complexity Justification**: N/A - No constitution violations

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-todo-chatbot/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research outcomes
├── data-model.md        # Phase 1 data model design
├── quickstart.md        # Phase 1 setup guide
├── contracts/           # Phase 1 API contracts
│   ├── chat-api.yaml    # POST /api/{user_id}/chat OpenAPI spec
│   └── mcp-tools.yaml   # MCP tool schemas
└── checklists/          # Quality validation
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
phase3/
├── backend/
│   ├── src/
│   │   ├── main.py                 # FastAPI application entry
│   │   ├── config.py               # Environment configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User SQLModel
│   │   │   ├── task.py             # Task SQLModel
│   │   │   ├── conversation.py     # Conversation SQLModel
│   │   │   └── message.py          # Message SQLModel
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── middleware.py       # JWT auth middleware
│   │   │   └── chat.py             # POST /api/{user_id}/chat endpoint
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── runner.py           # OpenAI Agents SDK orchestration
│   │   │   └── prompts.py          # Agent system prompts
│   │   ├── mcp/
│   │   │   ├── __init__.py
│   │   │   ├── server.py           # MCP server implementation
│   │   │   └── tools.py            # MCP tool definitions
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── connection.py       # Neon PostgreSQL connection
│   │       └── operations.py       # Database CRUD operations
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_chat_api.py        # Chat endpoint tests
│   │   ├── test_mcp_tools.py       # MCP tool tests
│   │   ├── test_auth.py            # JWT auth tests
│   │   └── test_stateless.py       # Stateless behavior tests
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Main chat page
│   │   │   └── layout.tsx          # Root layout
│   │   ├── components/
│   │   │   └── TodoChat.tsx        # OpenAI ChatKit integration
│   │   └── lib/
│   │       └── api.ts              # API client
│   ├── package.json
│   └── .env.example
│
└── README.md                        # Project overview
```

**Structure Decision**: Web application structure selected because Phase III requires both frontend (OpenAI ChatKit) and backend (FastAPI). The frontend is a Next.js application using ChatKit, and backend is Python FastAPI with clear separation of concerns (API routes, agent logic, MCP tools, database operations).

## Complexity Tracking

No constitution violations - this section intentionally left empty.

## Architecture Overview

### End-to-End Request Flow

```
User → ChatKit UI → POST /api/{user_id}/chat
                    ↓
                JWT Middleware (verify token, extract user_id)
                    ↓
                Chat Endpoint Handler
                    ├─→ Load conversation history from DB
                    ├─→ Initialize OpenAI Agent with MCP tools
                    ├─→ Agent processes message + history
                    ├─→ Agent calls MCP tools (if needed)
                    │   └─→ MCP tools execute DB operations
                    ├─→ Agent generates response
                    ├─→ Save new message turn to DB
                    └─→ Return response to user
                         ↓
                    ChatKit UI displays response
```

### Component Responsibilities

| Component | Responsibility | Must NOT Do |
|-----------|---------------|-------------|
| ChatKit UI | Render chat interface, send user messages, display agent responses | Business logic, direct API calls to other endpoints |
| FastAPI Endpoint | Authenticate, orchestrate agent, persist conversation | Hold conversation state in memory, access DB directly for tasks |
| OpenAI Agent | Understand intent, decide which tools to call, generate natural language responses | Access database directly, maintain state |
| MCP Tools | Execute deterministic task operations, return structured results | Make decisions, access data outside user scope |
| Database | Persist users, tasks, conversations, messages | N/A (storage only) |

## Key Architectural Decisions

### Decision 1: Stateless Conversation Handling

**Options Considered**:
1. **In-memory conversation cache** - Store recent conversations in Redis/memory
2. **Database persistence only** - Store and retrieve all conversation history from Neon PostgreSQL
3. **Hybrid** - Recent conversations in memory, older in database

**Tradeoffs**:

| Approach | Simplicity | Safety | Scalability |
|----------|------------|--------|-------------|
| In-memory | ❌ Complex sync | ❌ Data loss on restart | ❌ Single-server bound |
| DB-only | ✅ Simple | ✅ No data loss | ✅ Horizontal scaling |
| Hybrid | ❌ Most complex | ⚠️ Partial loss risk | ⚠️ Cache invalidation issues |

**Final Choice**: **Database persistence only**

**Rationale**: Constitution Principle III mandates zero in-memory state. Database-only approach ensures:
- Server can restart anytime without losing conversations
- Horizontal scaling works immediately (stateless)
- No cache invalidation complexity
- Simpler debugging and auditing
- Neon PostgreSQL performance sufficient for <3s response time requirement

### Decision 2: Agent Intent Resolution Strategy

**Options Considered**:
1. **Deterministic keyword matching** - Parse user input with regex/rules to map to tools
2. **Pure LLM-based** - Let OpenAI Agent SDK decide which tools to call based on description
3. **Hybrid** - Keywords for common patterns, LLM for complex cases

**Tradeoffs**:

| Approach | Simplicity | Safety | Scalability |
|----------|------------|--------|-------------|
| Deterministic | ✅ Predictable | ✅ Auditable | ❌ Rigid, poor UX |
| Pure LLM | ✅ Natural language | ⚠️ Non-deterministic | ✅ Flexible |
| Hybrid | ❌ Complex logic | ⚠️ Partial determinism | ⚠️ Inconsistent |

**Final Choice**: **Pure LLM-based (OpenAI Agents SDK)**

**Rationale**: Constitution Principle I requires deterministic behavior via tool calls, not intent resolution. The determinism comes from:
- Agent MUST use MCP tools for all task operations (no direct DB access)
- MCP tools have fixed schemas and deterministic implementations
- Agent's tool choice is logged and auditable
- Natural language understanding is the feature's value proposition

Trade-off: Slight non-determinism in tool selection is acceptable because:
- Spec requires 95% correct interpretation (SC-006)
- Agent can request clarification for ambiguous commands (FR-013)
- All tool executions are logged for audit

### Decision 3: MCP Tool Granularity

**Options Considered**:
1. **Single-task tools** - One tool per operation: add_task, list_tasks, update_task, complete_task, delete_task
2. **Composed tool chains** - High-level tools that call multiple operations: add_multiple_tasks, complete_and_archive
3. **Generic CRUD tool** - One tool with "operation" parameter: execute_task_operation(operation, data)

**Tradeoffs**:

| Approach | Simplicity | Safety | Scalability |
|----------|------------|--------|-------------|
| Single-task | ✅ Clear boundaries | ✅ Easy to validate | ✅ Composable |
| Composed chains | ❌ Complex logic in tools | ⚠️ Harder to audit | ❌ Tight coupling |
| Generic CRUD | ❌ Parameter parsing | ❌ Validation complexity | ❌ Poor observability |

**Final Choice**: **Single-task tools**

**Rationale**:
- Constitution Tooling Standards specify 5 required tools (add_task, list_tasks, update_task, complete_task, delete_task)
- Each tool has single responsibility, easy to test independently
- Agent composes tools naturally (e.g., list then complete)
- Clear audit trail: "Agent called add_task with {'title': 'buy groceries'}"
- Simpler to validate each tool's implementation

### Decision 4: Confirmation Strategy for Destructive Actions

**Options Considered**:
1. **No confirmation** - Delete immediately when user requests
2. **Tool-level confirmation** - MCP delete_task tool requires confirmation parameter
3. **Agent-level confirmation** - Agent asks user "Are you sure?" before calling delete tool
4. **UI-level confirmation** - ChatKit shows confirmation dialog

**Tradeoffs**:

| Approach | Simplicity | Safety | Scalability |
|----------|------------|--------|-------------|
| No confirmation | ✅ Fast | ❌ Accidental deletes | ✅ No state |
| Tool-level | ❌ Stateful confirmation | ⚠️ Moderate safety | ❌ Confirmation state |
| Agent-level | ✅ Natural conversation | ✅ Clear intent | ✅ Stateless |
| UI-level | ❌ Breaks chat paradigm | ⚠️ UI complexity | ✅ Client-side |

**Final Choice**: **Agent-level confirmation (conversational)**

**Rationale**:
- Maintains natural language interaction model
- Agent responds: "Are you sure you want to delete 'buy groceries'? Say 'yes' to confirm."
- User confirms in next message, agent calls delete_task tool
- Stateless: Confirmation context is in conversation history (reconstructed from DB)
- Aligns with spec requirement for friendly, conversational responses

### Decision 5: Error Handling for Ambiguous Commands

**Options Considered**:
1. **Best-guess execution** - Agent picks most likely interpretation and executes
2. **Request clarification** - Agent asks user to specify what they meant
3. **Suggest options** - Agent presents multiple interpretations for user to choose

**Tradeoffs**:

| Approach | Simplicity | Safety | Scalability |
|----------|------------|--------|-------------|
| Best-guess | ✅ Fast | ❌ Wrong actions | ✅ No follow-up |
| Request clarification | ✅ Safe | ✅ User control | ⚠️ Extra messages |
| Suggest options | ⚠️ Complex | ✅ Safe | ⚠️ Extra messages |

**Final Choice**: **Request clarification** (with option suggestions when possible)

**Rationale**:
- Spec FR-013: "System MUST handle ambiguous commands by requesting clarification"
- Constitution Principle I: No autonomous actions without user instruction
- Agent responds: "I found multiple tasks with 'buy' in the title. Which one did you mean: 1) buy groceries, 2) buy milk?"
- User provides clarification in next message
- Safer than guessing, maintains user control

### Decision 6: Conversation Resume Strategy

**Options Considered**:
1. **conversation_id in URL** - POST /api/{user_id}/chat/{conversation_id}
2. **conversation_id in request body** - {"message": "...", "conversation_id": "..."}
3. **Auto-resume last conversation** - Backend always uses user's most recent conversation
4. **New conversation per request** - No conversation continuity

**Tradeoffs**:

| Approach | Simplicity | Safety | Scalability |
|----------|------------|--------|-------------|
| URL-based | ✅ RESTful | ✅ Explicit | ✅ Cacheable |
| Body-based | ✅ Simple | ✅ Explicit | ✅ Simple |
| Auto-resume | ✅ No ID needed | ⚠️ No multi-conversation | ✅ Simple |
| No continuity | ✅ Stateless | ❌ No context | ✅ Simple |

**Final Choice**: **Auto-resume last conversation**

**Rationale**:
- Spec scope: Single ongoing conversation per user (no multi-conversation support in MVP)
- Simplifies frontend: No conversation ID management needed
- Backend logic: Load most recent conversation for user_id from database
- Future: Add conversation_id parameter if multi-conversation needed
- Maintains stateless architecture (conversation loaded from DB each time)

### Decision 7: Security Check Placement

**Options Considered**:
1. **Middleware only** - JWT validation and user_id matching in FastAPI middleware
2. **Tool-level only** - Each MCP tool validates user_id for data access
3. **Both layers** - Middleware + tool-level validation (defense in depth)

**Tradeoffs**:

| Approach | Simplicity | Safety | Scalability |
|----------|------------|--------|-------------|
| Middleware only | ✅ Single point | ⚠️ No defense in depth | ✅ Fast |
| Tool-level only | ❌ Repeated code | ⚠️ No early rejection | ❌ Slower |
| Both layers | ⚠️ Two checks | ✅ Defense in depth | ⚠️ Slight overhead |

**Final Choice**: **Both layers (defense in depth)**

**Rationale**:
- Constitution Principle V: "Security-first design"
- **Middleware layer**: Validates JWT, extracts user_id, ensures user_id in JWT matches route parameter
  - Rejects unauthenticated requests before reaching agent
  - Sets authenticated user_id in request context
- **Tool layer**: Every MCP tool accepts user_id parameter, filters all database queries by user_id
  - Prevents cross-user data access even if middleware bypassed
  - Explicit user isolation at data access level
- Minimal overhead (<10ms per request)
- Provides audit trail at both layers

## Phase 0: Research

[See research.md for detailed findings]

**Key Research Questions**:
1. OpenAI Agents SDK: How to integrate MCP tools with OpenAI Agent?
2. MCP SDK: How to define and expose custom tools?
3. Conversation persistence: Best schema for storing conversation history with message ordering?
4. Better Auth + FastAPI: JWT validation middleware implementation?
5. Neon PostgreSQL: Connection pooling and async operations with SQLModel?
6. OpenAI ChatKit: Integration with custom backend API?

## Phase 1: Design

[See data-model.md, contracts/, quickstart.md for detailed designs]

**Key Deliverables**:
- Data model for User, Task, Conversation, Message entities
- OpenAPI specification for POST /api/{user_id}/chat
- MCP tool schemas for 5 task operations
- Quickstart guide for local development setup

## Testing Strategy

### Functional Testing

| Test Category | Test Cases | Success Criteria |
|---------------|------------|------------------|
| Natural Language Commands | "Add task", "Show tasks", "Complete X", "Update Y", "Delete Z" | All 5 operations work via NL |
| Intent Mapping | Variations: "Create", "Make", "New task", "Add to list" | 95%+ correct tool selection |
| User Isolation | User A cannot access User B's tasks | 100% isolation |
| Conversation Context | Multi-turn conversations maintain context | Context preserved across 10+ turns |
| Stateless Behavior | Server restart mid-conversation | No data loss, conversation resumes |
| Error Handling | Invalid commands, missing tasks, ambiguity | User-friendly errors, no stack traces |

### Performance Testing

- Response time: 95% of requests complete in <3 seconds
- Concurrent users: 100 users simultaneously without degradation
- Database queries: <500ms per task operation

### Security Testing

- JWT validation: Expired/invalid tokens rejected
- User ID matching: JWT user_id must match route parameter
- Cross-user access: Attempts to access other user's data fail
- SQL injection: MCP tools use parameterized queries

## Implementation Phases (High-Level)

**Phase 2**: Task generation via /sp.tasks (not part of this document)

**Phase 3**: Implementation (follows task list from phase 2)
- Setup: Project structure, dependencies, environment
- Foundation: Database models, connection, migrations
- MCP Layer: Implement 5 MCP tools with schemas
- Agent Layer: OpenAI Agent integration with MCP tools
- API Layer: Chat endpoint with JWT middleware
- Frontend: ChatKit integration with backend
- Testing: Functional, security, performance tests
- Validation: Constitution compliance, spec adherence

## Next Steps

1. Review and approve this plan
2. Proceed to Phase 0: Run `/sp.plan` research phase to generate research.md
3. Proceed to Phase 1: Generate data-model.md, contracts/, quickstart.md
4. Run `/sp.tasks` to generate implementation task list
5. Execute implementation via `/sp.implement`

## Notes

- All design decisions aligned with constitution principles
- Stateless architecture enables cloud-native deployment
- MCP tools provide deterministic, auditable task operations
- OpenAI Agents SDK handles natural language understanding
- Security enforced at multiple layers (middleware + tools)
- Conversation persistence enables context across server restarts
