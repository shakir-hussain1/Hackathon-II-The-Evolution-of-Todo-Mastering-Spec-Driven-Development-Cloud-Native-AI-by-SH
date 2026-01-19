---
id: PHR-001-ai-todo-chatbot-002
stage: plan
feature: 001-ai-todo-chatbot
title: Implementation Plan
date: 2026-01-13
agent: Claude Sonnet 4.5
---

## Prompt Text

```text
/sp.plan Create:
- End-to-end architecture sketch for the AI-powered Todo Chatbot
  (ChatKit UI → FastAPI → OpenAI Agents SDK → MCP Server → Neon DB)
- Spec section structure for:
  - Chat API contract
  - Agent behavior and intent mapping
  - MCP tool definitions
  - Conversation persistence model
  - Security and authorization rules
- Execution flow for a stateless chat request cycle
- Quality validation framework mapped to acceptance criteria

Decisions needing documentation:
- Stateless conversation handling (DB persistence vs in-memory)
- Agent intent resolution strategy (deterministic vs hybrid)
- MCP tool granularity (single-task tools vs composed tool chains)
- Confirmation strategy for destructive actions
- Error handling for ambiguous or incomplete user commands
- Conversation resume strategy using conversation_id
- Placement of security checks (middleware vs tool-level)

For each decision:
- Options considered
- Tradeoffs (simplicity, safety, scalability)
- Final choice with rationale

Execution phases:
1. Foundation - Review Phase II APIs, auth, and database schema
2. Architecture - Design stateless chat endpoint, define Agent + MCP boundaries
3. Agent & MCP Design - Define agent behavior rules, specify MCP tools
4. Frontend Integration - Design ChatKit-based UI flow
5. Validation & Safety - Enforce JWT, user isolation, confirm destructive actions

Testing strategy:
- Validate each natural language command maps to correct MCP tool
```

## Response Summary

Successfully completed Phase 0 (Research) and Phase 1 (Design) for AI-Powered Todo Chatbot implementation planning.

### Deliverables Created

1. **Implementation Plan**: `specs/001-ai-todo-chatbot/plan.md`
   - Technical context and constitution compliance
   - End-to-end architecture with component responsibilities
   - 7 key architectural decisions with full rationale
   - Testing strategy and implementation phases

2. **Research Document**: `specs/001-ai-todo-chatbot/research.md`
   - OpenAI Agents SDK + MCP integration patterns
   - MCP tool definition using official SDK
   - Conversation persistence schema design
   - Better Auth + FastAPI JWT validation
   - Neon PostgreSQL + SQLModel async operations
   - OpenAI ChatKit integration approach

3. **Data Model**: `specs/001-ai-todo-chatbot/data-model.md`
   - 4 entities: User, Conversation, Message, Task
   - Complete SQLModel schemas with relationships
   - Database constraints and indexes
   - Query patterns with performance expectations
   - Migration strategy

4. **API Contracts**:
   - `specs/001-ai-todo-chatbot/contracts/chat-api.yaml` - OpenAPI specification for POST /api/{user_id}/chat
   - `specs/001-ai-todo-chatbot/contracts/mcp-tools.yaml` - MCP tool schemas for 5 task operations

5. **Quickstart Guide**: `specs/001-ai-todo-chatbot/quickstart.md`
   - Complete local development setup
   - Environment variable configuration
   - Database setup and testing
   - Common issues and solutions

### Architectural Decisions (All Resolved)

| Decision | Final Choice | Key Rationale |
|----------|-------------|---------------|
| Conversation Handling | Database persistence only | Constitution mandates stateless, supports horizontal scaling |
| Intent Resolution | Pure LLM-based (OpenAI Agents SDK) | Determinism at tool level, not intent resolution; natural language is value prop |
| MCP Tool Granularity | Single-task tools (5 separate tools) | Clear boundaries, easy validation, composable by agent |
| Destructive Confirmations | Agent-level conversational | Maintains chat paradigm, stateless (context in DB) |
| Ambiguous Commands | Request clarification | Constitution requires user control, safer than guessing |
| Conversation Resume | Auto-resume last conversation | MVP: single conversation per user, simplifies UX |
| Security Placement | Both middleware + tool layers | Defense in depth, security-first principle |

### Constitution Check Status

**Initial Check** (Pre-Design): ✅ ALL PRINCIPLES PASSED
**Post-Design Check**: ✅ ALL PRINCIPLES PASSED

All 6 core principles satisfied:
- Deterministic AI Behavior (MCP tools only)
- Spec-Driven Reproducibility (15 FRs documented)
- Stateless Architecture (DB-only persistence)
- Separation of Concerns (clear layer boundaries)
- Security-First Design (JWT + user isolation at both layers)
- Graceful Error Handling (user-friendly messages specified)

### Technology Stack Confirmed

- **Frontend**: Next.js 14+ with OpenAI ChatKit
- **Backend**: FastAPI 0.104+ (Python 3.11+)
- **AI Agent**: OpenAI Agents SDK
- **Tool Protocol**: Official MCP SDK
- **ORM**: SQLModel 0.0.14+ (async)
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth (JWT)
- **Testing**: pytest + httpx

### Request Flow Architecture

```
User Message
  ↓
ChatKit UI (Next.js)
  ↓ POST /api/{user_id}/chat + JWT
FastAPI Middleware
  ├─ Validate JWT
  ├─ Verify user_id match
  └─ Extract authenticated user_id
     ↓
Chat Endpoint Handler
  ├─ Load conversation history (DB)
  ├─ Initialize OpenAI Agent with MCP tools
  ├─ Agent processes message + history
  ├─ Agent calls MCP tools (if needed)
  │   └─ MCP tools → Database operations
  ├─ Agent generates response
  ├─ Save message turn to DB
  └─ Return response
     ↓
ChatKit UI displays response
```

### Data Model Summary

- **User**: Email, password_hash, timestamps
- **Conversation**: user_id (FK), title, timestamps
- **Message**: conversation_id (FK), role (user|assistant), content, tool_calls (JSONB), sequence_number
- **Task**: user_id (FK), title, description, status (pending|completed), timestamps

**Key Design Decisions**:
- UUID primary keys for distributed systems
- sequence_number for reliable message ordering
- JSONB tool_calls for audit trail
- ON DELETE CASCADE for data consistency

### Next Steps

1. **Task Generation**: Run `/sp.tasks` to create implementation task list
2. **Implementation**: Execute tasks via `/sp.implement`
3. **Quality Gates**:
   - backend-architect agent (FastAPI validation)
   - auth-security-validator agent (JWT + user isolation)
   - qa-validator agent (functional testing)
   - spec-compliance-enforcer agent (verify all FRs met)

## Artifacts Generated

- `specs/001-ai-todo-chatbot/plan.md` - Implementation plan (this file's primary output)
- `specs/001-ai-todo-chatbot/research.md` - Technical research findings
- `specs/001-ai-todo-chatbot/data-model.md` - Database schema and SQLModel definitions
- `specs/001-ai-todo-chatbot/contracts/chat-api.yaml` - Chat endpoint OpenAPI spec
- `specs/001-ai-todo-chatbot/contracts/mcp-tools.yaml` - MCP tool schemas
- `specs/001-ai-todo-chatbot/quickstart.md` - Local development setup guide
- `history/prompts/001-ai-todo-chatbot/002-implementation-plan.prompt.md` - This PHR
