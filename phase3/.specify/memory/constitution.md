<!--
SYNC IMPACT REPORT:
Version: 1.0.0 (Initial ratification)
Modified Principles: N/A (initial version)
Added Sections: All sections (initial creation)
Removed Sections: None
Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - Reviewed, aligns with constitution
  ✅ .specify/templates/spec-template.md - Reviewed, aligns with constitution
  ✅ .specify/templates/tasks-template.md - Reviewed, aligns with constitution
Follow-up TODOs: None
-->

# Phase III AI-Powered Todo Chatbot Constitution

## Core Principles

### I. Deterministic AI Behavior

**Rule**: No autonomous or uncontrolled AI actions are permitted.

Every AI agent action MUST be explicitly triggered by a user request and map to a
documented MCP tool call. The system MUST NOT make decisions, take actions, or
modify data without direct user instruction. All agent behavior MUST be traceable
to specific tool invocations.

**Rationale**: Deterministic behavior ensures predictability, auditability, and user
trust. Users must maintain full control over their data and actions at all times.

### II. Spec-Driven Reproducibility

**Rule**: Every behavior MUST be traceable to specifications.

All features, behaviors, and system responses MUST be documented in specification
files before implementation. No undocumented features or behaviors are permitted.
Changes to behavior require corresponding specification updates.

**Rationale**: Spec-driven development ensures reproducible builds, clear
expectations, and maintainable code. It enables AI agents to produce consistent
results when given the same specifications.

### III. Stateless, Cloud-Native Architecture

**Rule**: Zero in-memory conversational state permitted on the server.

The FastAPI backend MUST NOT hold any conversational state in memory. All state
MUST be persisted to the database immediately. The server must be restartable at
any time without loss of conversation context or user data. Every request MUST be
self-contained and authenticated.

**Rationale**: Stateless architecture enables horizontal scaling, fault tolerance,
and serverless deployment. It eliminates single points of failure and supports
modern cloud-native patterns.

### IV. Separation of Concerns

**Rule**: Clear boundaries between UI, Agent reasoning, MCP tools, and persistence.

- **Frontend (OpenAI ChatKit)**: UI rendering and user interaction only
- **Agent (OpenAI Agents SDK)**: Reasoning and tool orchestration only
- **MCP Tools**: Stateless operations with database persistence only
- **Database (Neon PostgreSQL)**: Single source of truth for all state

No layer may bypass or assume responsibilities of another layer. The AI agent MUST
NOT access the database directly; all persistence goes through MCP tools.

**Rationale**: Separation of concerns enables independent testing, clear interfaces,
and maintainable architecture. Each layer can evolve independently without affecting
others.

### V. Security-First Design

**Rule**: Strict user isolation and authentication enforcement on every request.

Every API request MUST be authenticated via Better Auth JWT. The user_id in the JWT
MUST match the user_id in the API route parameter. All database queries MUST filter
by user_id to enforce data isolation. Cross-user data access is NEVER permitted.

**Rationale**: Security-first design prevents data leaks, unauthorized access, and
privilege escalation. User isolation is fundamental to multi-tenant SaaS applications.

### VI. Graceful Error Handling

**Rule**: All errors MUST be handled gracefully with user-friendly responses.

System errors, tool failures, and validation errors MUST be caught and transformed
into clear, actionable messages for users. Technical stack traces MUST NOT be
exposed to users. The agent MUST acknowledge errors and suggest corrective actions.

**Rationale**: Graceful error handling improves user experience, maintains trust,
and prevents confusion. Users should never see cryptic technical errors.

## Tooling Standards

### MCP Tool Requirements

All MCP tools MUST be stateless and conform to the following schema:

**Required Tools**:
- `add_task`: Create new task (input: title, description, user_id | output: task object)
- `list_tasks`: Retrieve all tasks for user (input: user_id | output: task array)
- `update_task`: Modify existing task (input: task_id, updates, user_id | output: updated task)
- `complete_task`: Mark task as complete (input: task_id, user_id | output: success)
- `delete_task`: Remove task (input: task_id, user_id | output: success)

**Tool Standards**:
- All tools MUST accept user_id for isolation enforcement
- All tools MUST validate inputs and return structured responses
- All tools MUST persist state to database (no in-memory caching)
- All tools MUST return human-readable success/error messages
- Tool composition is allowed but MUST remain auditable

**Agent Confirmation**:
The AI agent MUST confirm all task mutations with friendly, natural language
responses that summarize what was done (e.g., "I've added 'Buy groceries' to
your task list").

## Architecture Rules

### Single Stateless Endpoint

**Rule**: POST /api/{user_id}/chat is the only conversational endpoint.

This endpoint MUST:
- Authenticate the request via Better Auth JWT
- Verify user_id in JWT matches user_id in route parameter
- Reconstruct conversation context from database
- Execute agent reasoning with MCP tool access
- Persist new conversation turns to database
- Return agent response

The endpoint MUST NOT maintain any state between requests.

### Technology Stack Enforcement

**Frontend**: OpenAI ChatKit MUST be used for all chat UI components. No custom
chat interfaces are permitted unless explicitly justified.

**Backend**: Python FastAPI MUST be used for the API server. The server MUST
orchestrate agent execution and MCP tool calls.

**AI Framework**: OpenAI Agents SDK MUST be used exclusively for agent logic. No
custom agent implementations or alternative frameworks permitted.

**MCP Server**: Official MCP SDK MUST be used to expose task management tools.

**ORM**: SQLModel MUST be used for all database operations.

**Database**: Neon Serverless PostgreSQL MUST be used for all persistence.

**Authentication**: Better Auth with JWT MUST be used for all authentication.

## Development Constraints

### Spec-Kit Plus Workflow (Mandatory)

All development MUST follow the Agentic Dev Stack workflow:

1. **Spec**: Define feature requirements in spec.md using Spec-Kit Plus
2. **Plan**: Create implementation plan in plan.md with technical approach
3. **Tasks**: Generate task list in tasks.md with dependencies
4. **Implement**: Execute tasks via AI agents (Claude Code)

**Manual coding is prohibited**. All code MUST be generated by AI agents following
specifications. If the generated code is incorrect, the specifications MUST be
refined until correct output is produced.

### Reusable Intelligence

Complex, repeated operations MUST be captured as:
- **Subagents**: For multi-step workflows requiring context and decision-making
- **Skills**: For single-purpose, parameterized operations

Ad-hoc scripting for repeated tasks is discouraged.

## Non-Goals

The following are explicitly OUT OF SCOPE for this project:

- **Autonomous AI behavior**: Agent cannot take actions without explicit user request
- **Real-time collaboration**: Multi-user editing or live presence features
- **Offline functionality**: Application requires internet connection
- **Mobile native apps**: Web-only, no iOS/Android native builds
- **Complex task dependencies**: No Gantt charts, critical paths, or dependency graphs
- **Time tracking**: No timers, time estimates, or productivity analytics
- **File attachments**: Tasks are text-only, no file uploads
- **Integrations**: No calendar sync, email integration, or third-party APIs
- **Custom agent frameworks**: Must use OpenAI Agents SDK exclusively

## Governance

### Amendment Procedure

Constitution amendments require:
1. Documented rationale for the change
2. Impact analysis on existing specifications and code
3. Approval from project maintainers
4. Migration plan for existing implementations
5. Version bump following semantic versioning

### Version Policy

- **MAJOR**: Backward incompatible principle changes (e.g., removing security rules)
- **MINOR**: New principles added or existing ones materially expanded
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Compliance Review

All pull requests MUST verify compliance with this constitution. Any complexity
or deviation MUST be explicitly justified and documented. Code reviews MUST
include constitution compliance checks.

### Runtime Guidance

For runtime development guidance and agent-specific instructions, refer to
`CLAUDE.md` in the project root.

**Version**: 1.0.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-13
