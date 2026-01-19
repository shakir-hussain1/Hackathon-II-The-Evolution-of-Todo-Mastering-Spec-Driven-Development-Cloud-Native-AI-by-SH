# Research: AI-Powered Todo Chatbot

**Date**: 2026-01-13
**Feature**: 001-ai-todo-chatbot
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Research Questions & Findings

### 1. OpenAI Agents SDK + MCP Tool Integration

**Question**: How to integrate custom MCP tools with OpenAI Agents SDK?

**Research Findings**:

The OpenAI Agents SDK (also called "Swarm" in some documentation) supports function calling, which is the mechanism used for tool integration. Key integration pattern:

```python
# Define MCP tool as Python function
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Add a new task to user's todo list"""
    # MCP server handles actual implementation
    return mcp_client.call_tool("add_task", {
        "user_id": user_id,
        "title": title,
        "description": description
    })

# Register with OpenAI Agent
agent = Agent(
    name="Todo Assistant",
    model="gpt-4",
    instructions="You help users manage their todo lists...",
    functions=[add_task, list_tasks, update_task, complete_task, delete_task]
)
```

**Decision**: Use OpenAI function calling as bridge between Agent and MCP tools
- Agent sees tools as Python functions with docstrings
- Function implementations delegate to MCP server via MCP SDK client
- Provides clean separation: Agent reasoning vs. Tool execution

**Alternatives Considered**:
- Direct MCP protocol in Agent: Too complex, couples agent to MCP implementation
- Langchain Tool wrappers: Unnecessary abstraction layer

### 2. MCP SDK Tool Definition

**Question**: How to define and expose custom MCP tools using official MCP SDK?

**Research Findings**:

MCP SDK provides decorator-based tool registration:

```python
from mcp import Server, Tool

server = Server("todo-mcp-server")

@server.tool("add_task")
async def add_task(
    user_id: str,
    title: str,
    description: str = ""
) -> dict:
    """
    Add a new task to the user's todo list.

    Args:
        user_id: Unique identifier for the user
        title: Task title/description
        description: Optional detailed description

    Returns:
        Created task object with id, title, description, status, created_at
    """
    # Implementation here
    task = await db.create_task(user_id, title, description)
    return {
        "success": True,
        "task": task.dict(),
        "message": f"Added task: {title}"
    }
```

**Decision**: Use MCP SDK decorators for tool definition
- Type hints provide automatic schema generation
- Docstrings become tool descriptions for Agent
- Async support for database operations

**Tool Schema Standard**:
All MCP tools follow this response schema:
```json
{
  "success": boolean,
  "data": object | array,
  "message": string,
  "error": string | null
}
```

### 3. Conversation Persistence Schema

**Question**: Best database schema for storing conversation history with proper message ordering?

**Research Findings**:

**Schema Design**:

```
users
├── id (UUID, PK)
├── email (string, unique)
├── password_hash (string)
├── created_at (timestamp)
└── updated_at (timestamp)

conversations
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── title (string, nullable) # "Todo List Discussion"
├── created_at (timestamp)
└── updated_at (timestamp)

messages
├── id (UUID, PK)
├── conversation_id (UUID, FK → conversations.id)
├── role (enum: 'user' | 'assistant')
├── content (text)
├── tool_calls (JSONB, nullable) # Records which MCP tools were called
├── created_at (timestamp)
└── sequence_number (integer) # For ordering within conversation

tasks
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── title (string)
├── description (text, nullable)
├── status (enum: 'pending' | 'completed')
├── created_at (timestamp)
├── updated_at (timestamp)
└── completed_at (timestamp, nullable)
```

**Key Design Decisions**:

1. **sequence_number vs. timestamp ordering**:
   - Use sequence_number (integer) for reliable message ordering
   - Timestamps can collide in high-throughput scenarios
   - Sequence increments atomically per conversation

2. **tool_calls as JSONB**:
   - Stores audit trail of MCP tool invocations
   - Schema: `[{"tool": "add_task", "args": {...}, "result": {...}}]`
   - Enables debugging and auditing

3. **One conversation per user (MVP)**:
   - Frontend always loads user's single ongoing conversation
   - Simplifies UX and backend logic
   - Future: Support multiple conversations if needed

**Decision**: Implement schema above with SQLModel
- UUID primary keys for distributed systems
- sequence_number for message ordering
- JSONB for flexible tool_calls storage
- Indexes on user_id and conversation_id for fast lookups

### 4. Better Auth + FastAPI JWT Validation

**Question**: How to implement JWT validation middleware with Better Auth in FastAPI?

**Research Findings**:

**Better Auth JWT Structure**:
```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234571490
}
```

**FastAPI Middleware Pattern**:

```python
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Verify JWT token and return payload"""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

# Use in endpoint
@app.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    payload: dict = Depends(verify_jwt)
):
    # Verify user_id matches token
    if payload["sub"] != user_id:
        raise HTTPException(403, "User ID mismatch")
    # Continue...
```

**Decision**: Use FastAPI Depends() for JWT validation
- Clean dependency injection pattern
- Automatic token extraction from Authorization header
- Centralized error handling
- user_id matching enforced in endpoint

**Secret Management**:
- JWT_SECRET loaded from environment variable
- Never commit secrets to git
- Use different secrets for dev/staging/prod

### 5. Neon PostgreSQL + SQLModel Async Operations

**Question**: How to handle connection pooling and async database operations with Neon Serverless PostgreSQL?

**Research Findings**:

**Connection Setup**:

```python
from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

# Async engine for FastAPI
engine = create_async_engine(
    settings.DATABASE_URL,  # postgresql+asyncpg://...
    echo=True,  # Log SQL in development
    pool_pre_ping=True,  # Verify connections before use
    pool_size=10,  # Connection pool size
    max_overflow=20  # Additional connections if pool exhausted
)

async def get_session() -> AsyncSession:
    """Dependency for database sessions"""
    async with AsyncSession(engine) as session:
        yield session
```

**Async Query Pattern**:

```python
async def create_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: str = ""
) -> Task:
    task = Task(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=title,
        description=description,
        status="pending"
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

**Decision**: Use async SQLModel with asyncpg driver
- Neon PostgreSQL supports standard PostgreSQL protocol
- asyncpg is fastest async driver for PostgreSQL
- SQLModel provides clean async API
- Connection pooling handles concurrent requests

**Connection String Format**:
```
postgresql+asyncpg://user:password@host/database?sslmode=require
```

### 6. OpenAI ChatKit Integration

**Question**: How to integrate OpenAI ChatKit with custom FastAPI backend?

**Research Findings**:

**ChatKit Architecture**:
- React component library for chat UI
- Handles message rendering, input, loading states
- Requires custom API adapter for backend integration

**Integration Pattern**:

```typescript
// frontend/src/lib/api.ts
export async function sendMessage(
  userId: string,
  message: string,
  token: string
): Promise<ChatResponse> {
  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message })
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json();
}

// frontend/src/components/TodoChat.tsx
import { ChatContainer, MessageList, MessageInput } from '@openai/chatkit';

export function TodoChat() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text: string) => {
    const userMsg = { role: 'user', content: text };
    setMessages([...messages, userMsg]);

    const response = await sendMessage(userId, text, token);
    const assistantMsg = {
      role: 'assistant',
      content: response.message
    };
    setMessages([...messages, userMsg, assistantMsg]);
  };

  return (
    <ChatContainer>
      <MessageList messages={messages} />
      <MessageInput onSend={handleSend} />
    </ChatContainer>
  );
}
```

**Decision**: Use ChatKit with custom API adapter
- ChatKit handles UI/UX (message rendering, loading, errors)
- Custom adapter calls POST /api/{user_id}/chat
- Frontend manages optimistic updates (show user message immediately)
- Backend response updates assistant message

**State Management**:
- ChatKit manages message array in React state
- Conversation history loaded on mount from backend
- No Redux/Zustand needed for MVP (ChatKit is self-contained)

## Best Practices Summary

### OpenAI Agents SDK
- Define clear agent instructions (system prompt)
- Register tools as Python functions with docstrings
- Use structured outputs (Pydantic models) for type safety
- Log all agent decisions and tool calls

### MCP Tool Design
- Single responsibility per tool (add_task, not manage_tasks)
- Accept user_id for all operations (enforce isolation)
- Return structured responses with success/error/message
- Use async for database operations
- Validate inputs before execution

### FastAPI Patterns
- Use Depends() for auth, database sessions
- Async endpoints for I/O operations
- Structured error responses (FastAPI HTTPException)
- CORS middleware for frontend communication
- Pydantic models for request/response validation

### Database Operations
- Always filter by user_id (user isolation)
- Use transactions for multi-step operations
- Index foreign keys (user_id, conversation_id)
- Use UUID for distributed ID generation

### Security
- JWT secret in environment variables
- Verify user_id matches JWT claim
- HTTPS only in production
- Rate limiting for chat endpoint (prevent abuse)
- Parameterized queries (SQL injection prevention)

### Testing
- Unit tests: MCP tools in isolation
- Integration tests: Chat endpoint with mocked agent
- E2E tests: Full flow with real database
- Security tests: JWT validation, user isolation

## Technology Stack Confirmation

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Frontend Framework | Next.js | 14+ | React framework with SSR, required for ChatKit |
| Chat UI | OpenAI ChatKit | Latest | Official chat component library |
| Backend Framework | FastAPI | 0.104+ | Async Python, OpenAPI docs, best for AI APIs |
| AI Agent | OpenAI Agents SDK | Latest | Official SDK for agent orchestration |
| Tool Protocol | MCP SDK | Official | Standardized tool invocation protocol |
| ORM | SQLModel | 0.0.14+ | SQLAlchemy + Pydantic, async support |
| Database | Neon PostgreSQL | Serverless | Cloud-native, auto-scaling, compatible with PostgreSQL |
| Auth | Better Auth | Latest | JWT-based auth for Next.js + FastAPI |
| Testing | pytest + httpx | Latest | Async testing for FastAPI |

## Unresolved Questions

None - all technical unknowns from plan.md resolved.

## Next Steps

1. Proceed to Phase 1: Generate data-model.md with SQLModel schemas
2. Generate contracts/chat-api.yaml with OpenAPI specification
3. Generate contracts/mcp-tools.yaml with MCP tool schemas
4. Generate quickstart.md with local development setup guide
5. Update agent context with Phase III technology stack
