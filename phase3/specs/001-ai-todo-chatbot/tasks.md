# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `specs/001-ai-todo-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, therefore test tasks are OMITTED.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/` (this project)
- Paths shown below use web app structure from plan.md

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure: backend/src/{models,api,agent,mcp,db}/, backend/tests/
- [x] T002 Create frontend directory structure: frontend/src/{app,components,lib}/
- [x] T003 [P] Initialize backend Python project with requirements.txt (FastAPI, OpenAI SDK, MCP SDK, SQLModel, asyncpg, python-jose, bcrypt, pytest)
- [x] T004 [P] Initialize frontend Next.js project with package.json (Next.js 14+, OpenAI ChatKit, @better-auth/react)
- [x] T005 [P] Create backend/.env.example with DATABASE_URL, OPENAI_API_KEY, JWT_SECRET, CORS_ORIGINS
- [x] T006 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
- [x] T007 [P] Configure linting and formatting tools (backend: black, flake8, frontend: eslint, prettier)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create backend/src/config.py for environment variables (DATABASE_URL, OPENAI_API_KEY, JWT_SECRET, CORS_ORIGINS)
- [x] T009 [P] Setup database connection in backend/src/db/connection.py (async engine with Neon PostgreSQL, connection pooling)
- [x] T010 [P] Create User SQLModel in backend/src/models/user.py (id, email, password_hash, created_at, updated_at)
- [x] T011 [P] Create Task SQLModel in backend/src/models/task.py (id, user_id FK, title, description, status enum, timestamps)
- [x] T012 [P] Create Conversation SQLModel in backend/src/models/conversation.py (id, user_id FK, title, timestamps)
- [x] T013 [P] Create Message SQLModel in backend/src/models/message.py (id, conversation_id FK, role enum, content, tool_calls JSONB, sequence_number, created_at)
- [x] T014 Create database migration script in backend/src/db/migrate.py (create all tables with indexes)
- [x] T015 Create Better Auth configuration in backend/src/api/auth.py (register, login endpoints with JWT generation)
- [x] T016 [P] Implement JWT middleware in backend/src/api/middleware.py (verify token, extract user_id, enforce user_id matching)
- [x] T017 Setup FastAPI application in backend/src/main.py (CORS middleware, auth middleware, error handlers)
- [x] T018 [P] Create database operations in backend/src/db/operations.py (CRUD functions for User, Task, Conversation, Message with user_id filtering)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Tasks via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks by describing them conversationally

**Independent Test**: User sends "Add buy groceries" and task appears with confirmation "I've added 'buy groceries' to your task list"

### Implementation for User Story 1

- [ ] T019 [P] [US1] Implement MCP server initialization in backend/src/mcp/server.py (using official MCP SDK)
- [ ] T020 [P] [US1] Implement add_task MCP tool in backend/src/mcp/tools.py (accepts user_id, title, description; returns task object)
- [ ] T021 [US1] Configure OpenAI Agent in backend/src/agent/runner.py (initialize agent with MCP tools, system prompt for task management)
- [ ] T022 [US1] Create agent system prompts in backend/src/agent/prompts.py (define agent behavior, tool usage rules, confirmation patterns)
- [ ] T023 [US1] Implement conversation loading in backend/src/db/operations.py (load_conversation_history function with message ordering)
- [ ] T024 [US1] Implement message persistence in backend/src/db/operations.py (save_user_message, save_assistant_message with tool_calls)
- [ ] T025 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat.py (accept message, load history, run agent, persist messages, return response)
- [ ] T026 [US1] Add error handling for agent failures in backend/src/api/chat.py (catch MCP tool errors, return user-friendly messages)
- [ ] T027 [US1] Add error handling for ambiguous commands in backend/src/agent/prompts.py (agent asks clarification questions)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can request to see their complete task list through natural language

**Independent Test**: User sends "Show me my tasks" and receives formatted list of all tasks

### Implementation for User Story 2

- [ ] T028 [P] [US2] Implement list_tasks MCP tool in backend/src/mcp/tools.py (accepts user_id, optional status filter; returns task array)
- [ ] T029 [US2] Update agent prompts in backend/src/agent/prompts.py (add list_tasks tool usage examples, formatting guidelines)
- [ ] T030 [US2] Add empty list handling in backend/src/agent/prompts.py (agent responds with friendly message when no tasks exist)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark tasks as complete through natural language

**Independent Test**: User says "Mark 'buy groceries' as complete" and task status updates with confirmation

### Implementation for User Story 3

- [ ] T031 [P] [US3] Implement complete_task MCP tool in backend/src/mcp/tools.py (accepts user_id, task_id; updates status to completed, sets completed_at)
- [ ] T032 [US3] Update agent prompts in backend/src/agent/prompts.py (add complete_task tool usage, task disambiguation logic)
- [ ] T033 [US3] Add task not found error handling in backend/src/mcp/tools.py (return user-friendly error for non-existent tasks)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Details (Priority: P2)

**Goal**: Users can modify existing task titles or descriptions through conversational commands

**Independent Test**: User says "Change 'buy groceries' to 'buy groceries and household items'" and task title updates with confirmation

### Implementation for User Story 4

- [ ] T034 [P] [US4] Implement update_task MCP tool in backend/src/mcp/tools.py (accepts user_id, task_id, optional title, optional description; updates task)
- [ ] T035 [US4] Update agent prompts in backend/src/agent/prompts.py (add update_task tool usage, handle partial updates)
- [ ] T036 [US4] Add validation for empty updates in backend/src/mcp/tools.py (require at least one field to update)

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Users can remove tasks from their list through natural language commands

**Independent Test**: User says "Delete the buy groceries task" and task is removed with confirmation

### Implementation for User Story 5

- [ ] T037 [P] [US5] Implement delete_task MCP tool in backend/src/mcp/tools.py (accepts user_id, task_id; deletes task from database)
- [ ] T038 [US5] Update agent prompts in backend/src/agent/prompts.py (add delete_task tool usage, confirmation for destructive actions)
- [ ] T039 [US5] Implement confirmation flow for bulk deletes in backend/src/agent/prompts.py (agent asks "Are you sure?" for "delete all completed tasks")

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Frontend Integration

**Purpose**: Integrate OpenAI ChatKit with backend API

- [ ] T040 [P] Install OpenAI ChatKit and dependencies in frontend (npm install @openai/chatkit)
- [ ] T041 [P] Create API client in frontend/src/lib/api.ts (sendMessage function with JWT auth, error handling)
- [ ] T042 Create TodoChat component in frontend/src/components/TodoChat.tsx (integrate ChatKit MessageList, MessageInput)
- [ ] T043 Implement conversation loading in frontend/src/components/TodoChat.tsx (load history from backend on mount)
- [ ] T044 Implement message sending in frontend/src/components/TodoChat.tsx (optimistic UI updates, handle backend response)
- [ ] T045 Add error display in frontend/src/components/TodoChat.tsx (show user-friendly error messages from backend)
- [ ] T046 Create main chat page in frontend/src/app/page.tsx (render TodoChat component with authentication check)
- [ ] T047 Add Better Auth integration in frontend/src/app/layout.tsx (session provider, authentication state)
- [ ] T048 Create login page in frontend/src/app/login/page.tsx (email/password form, JWT token storage)
- [ ] T049 Create signup page in frontend/src/app/signup/page.tsx (user registration form)

---

## Phase 9: Security & Polish

**Purpose**: Final security hardening and user experience improvements

- [ ] T050 [P] Add request rate limiting to chat endpoint in backend/src/api/middleware.py (prevent abuse, 60 requests/minute per user)
- [ ] T051 [P] Add comprehensive logging in backend/src/mcp/tools.py (log all tool invocations with user_id, tool name, args, result)
- [ ] T052 [P] Add audit trail in backend/src/db/operations.py (ensure tool_calls JSONB populated in messages)
- [ ] T053 Validate stateless behavior in backend/src/api/chat.py (ensure no in-memory state between requests)
- [ ] T054 [P] Add loading states to frontend in frontend/src/components/TodoChat.tsx (show spinner while agent processes)
- [ ] T055 [P] Add typing indicators to frontend in frontend/src/components/TodoChat.tsx (show "Assistant is typing..." while waiting)
- [ ] T056 Run quickstart.md validation (verify all setup steps work for new developers)
- [ ] T057 [P] Code cleanup and formatting (run black, flake8 on backend; eslint, prettier on frontend)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Frontend Integration (Phase 8)**: Depends on at least one user story being complete (recommend US1+US2)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Requires US2 for task disambiguation
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Requires US2 for task disambiguation
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Requires US2 for task disambiguation

### Within Each User Story

- MCP tools and agent configuration can run in parallel (different files)
- Conversation persistence before chat endpoint (endpoint depends on persistence functions)
- Error handling after core functionality implemented

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1 and 2 can start in parallel
- User Stories 3, 4, 5 can start in parallel after US2 completes (for disambiguation logic)
- All Frontend tasks marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# These tasks can run in parallel within US1:
# (Different files, no dependencies on each other)

Task T019: backend/src/mcp/server.py
Task T020: backend/src/mcp/tools.py (add_task tool)
Task T022: backend/src/agent/prompts.py

# These tasks must run sequentially:
# (Dependencies exist)

T021 depends on T019 (agent needs MCP server)
T025 depends on T021, T023, T024 (endpoint needs agent + persistence)
T026 depends on T025 (error handling for endpoint)
```

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Tasks)
4. Complete Phase 4: User Story 2 (View Tasks)
5. Complete Phase 8: Frontend Integration (basic)
6. **STOP and VALIDATE**: Test US1+US2 independently
7. Deploy/demo if ready

**Why this MVP**: US1+US2 provide core value (add and view tasks). Users can start managing tasks immediately. US3-US5 enhance the experience but aren't blocking for basic usage.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: can add tasks!)
3. Add User Story 2 → Test independently → Deploy/Demo (can add AND view!)
4. Add User Story 3 → Test independently → Deploy/Demo (can complete tasks!)
5. Add User Story 4 → Test independently → Deploy/Demo (can update tasks!)
6. Add User Story 5 → Test independently → Deploy/Demo (can delete tasks!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add Tasks)
   - Developer B: User Story 2 (View Tasks)
3. After US2 completes:
   - Developer A: User Story 3 (Complete Tasks)
   - Developer B: User Story 4 (Update Tasks)
   - Developer C: User Story 5 (Delete Tasks)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No tests included (not requested in specification)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Total Tasks**: 57
- **Phase 1 (Setup)**: 7 tasks
- **Phase 2 (Foundational)**: 11 tasks (BLOCKING)
- **Phase 3 (User Story 1)**: 9 tasks (P1 - MVP)
- **Phase 4 (User Story 2)**: 3 tasks (P1 - MVP)
- **Phase 5 (User Story 3)**: 3 tasks (P2)
- **Phase 6 (User Story 4)**: 3 tasks (P2)
- **Phase 7 (User Story 5)**: 3 tasks (P3)
- **Phase 8 (Frontend)**: 10 tasks
- **Phase 9 (Polish)**: 8 tasks

**Parallel Opportunities**: 25 tasks marked [P] can run in parallel (44% of total)

**MVP Scope** (Recommended): Phases 1-4 + Phase 8 (basic) = 30 tasks (53% of total)

**Independent Test Criteria**:
- US1: Send "Add buy groceries" → task created, confirmation received
- US2: Send "Show me my tasks" → formatted list displayed
- US3: Send "Mark buy groceries as complete" → status updated, confirmation received
- US4: Send "Change buy groceries to buy groceries and milk" → title updated, confirmation received
- US5: Send "Delete buy groceries" → task removed, confirmation received
