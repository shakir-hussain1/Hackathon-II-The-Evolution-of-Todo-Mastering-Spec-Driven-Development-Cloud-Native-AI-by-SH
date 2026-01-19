# Data Model: AI-Powered Todo Chatbot

**Date**: 2026-01-13
**Feature**: 001-ai-todo-chatbot
**Purpose**: Define database schema and entity relationships

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       │ 1:N
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌──────────────┐   ┌──────────┐
│ Conversation│    │     Task     │   │          │
└──────┬──────┘    └──────────────┘   └──────────┘
       │
       │ 1:N
       │
       ▼
┌─────────────┐
│   Message   │
└─────────────┘
```

## Entity Definitions

### User

Represents an authenticated user of the system.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique user identifier |
| email | String(255) | UNIQUE, NOT NULL | User's email address for authentication |
| password_hash | String(255) | NOT NULL | Bcrypt/Argon2 hashed password |
| created_at | Timestamp | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| updated_at | Timestamp | NOT NULL, DEFAULT NOW() | Last account update timestamp |

**Relationships**:
- One user has many conversations (1:N)
- One user has many tasks (1:N)

**Indexes**:
- PRIMARY KEY on id
- UNIQUE INDEX on email
- INDEX on created_at (for sorting)

**SQLModel Schema**:

```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversations: List["Conversation"] = Relationship(back_populates="user")
    tasks: List["Task"] = Relationship(back_populates="user")
```

**Validation Rules**:
- Email must be valid format (regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
- Password must be hashed before storage (never store plaintext)
- password_hash generated using bcrypt with cost factor 12

---

### Conversation

Represents a conversation thread between user and AI agent.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique conversation identifier |
| user_id | UUID | FK → users.id, NOT NULL | Owner of the conversation |
| title | String(500) | NULLABLE | Optional conversation title (e.g., "Todo List Discussion") |
| created_at | Timestamp | NOT NULL, DEFAULT NOW() | Conversation start timestamp |
| updated_at | Timestamp | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Relationships**:
- One conversation belongs to one user (N:1)
- One conversation has many messages (1:N)

**Indexes**:
- PRIMARY KEY on id
- INDEX on user_id (fast lookup for user's conversations)
- INDEX on updated_at (for sorting by recent activity)

**SQLModel Schema**:

```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id: str = Field(foreign_key="users.id", nullable=False)
    title: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Business Rules**:
- MVP: One active conversation per user (load most recent by updated_at)
- Title auto-generated from first user message (optional)
- updated_at refreshed on every new message

---

### Message

Represents a single message turn in a conversation (user or assistant).

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique message identifier |
| conversation_id | UUID | FK → conversations.id, NOT NULL | Parent conversation |
| role | Enum | NOT NULL, CHECK ('user', 'assistant') | Message sender role |
| content | Text | NOT NULL | Message content (user input or agent response) |
| tool_calls | JSONB | NULLABLE | Audit trail of MCP tool invocations |
| sequence_number | Integer | NOT NULL | Message order within conversation |
| created_at | Timestamp | NOT NULL, DEFAULT NOW() | Message timestamp |

**Relationships**:
- One message belongs to one conversation (N:1)

**Indexes**:
- PRIMARY KEY on id
- INDEX on conversation_id (fast lookup for conversation history)
- UNIQUE INDEX on (conversation_id, sequence_number) (prevent duplicates)
- INDEX on created_at (for sorting)

**SQLModel Schema**:

```python
from enum import Enum as PyEnum

class MessageRole(str, PyEnum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    conversation_id: str = Field(
        foreign_key="conversations.id",
        nullable=False
    )
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    tool_calls: Optional[dict] = Field(
        default=None,
        sa_column_kwargs={"type_": "JSONB"}
    )
    sequence_number: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**tool_calls Schema** (JSONB):

```json
{
  "calls": [
    {
      "tool": "add_task",
      "args": {
        "user_id": "uuid",
        "title": "buy groceries",
        "description": ""
      },
      "result": {
        "success": true,
        "task": {...},
        "message": "Added task: buy groceries"
      },
      "timestamp": "2026-01-13T10:30:00Z"
    }
  ]
}
```

**Business Rules**:
- sequence_number increments atomically per conversation
- tool_calls only populated for assistant messages that invoked tools
- Messages ordered by sequence_number (not created_at)

---

### Task

Represents a todo task created by user via chatbot.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique task identifier |
| user_id | UUID | FK → users.id, NOT NULL | Task owner |
| title | String(500) | NOT NULL | Task title/description |
| description | Text | NULLABLE | Optional detailed description |
| status | Enum | NOT NULL, DEFAULT 'pending', CHECK ('pending', 'completed') | Task status |
| created_at | Timestamp | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | Timestamp | NOT NULL, DEFAULT NOW() | Last task update timestamp |
| completed_at | Timestamp | NULLABLE | Task completion timestamp |

**Relationships**:
- One task belongs to one user (N:1)

**Indexes**:
- PRIMARY KEY on id
- INDEX on user_id (fast lookup for user's tasks)
- INDEX on status (filter by pending/completed)
- INDEX on created_at (for sorting)

**SQLModel Schema**:

```python
class TaskStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id: str = Field(foreign_key="users.id", nullable=False)
    title: str = Field(nullable=False, max_length=500)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # Relationships
    user: User = Relationship(back_populates="tasks")
```

**State Transitions**:

```
pending → completed (via complete_task MCP tool)
```

**Business Rules**:
- completed_at set when status changes to 'completed'
- updated_at refreshed on any field update
- Tasks soft-deleted (status changes, not removed) for audit trail
- Title limited to 500 characters (reasonable task description length)

---

## Database Constraints

### Foreign Keys

- conversations.user_id → users.id (ON DELETE CASCADE)
- messages.conversation_id → conversations.id (ON DELETE CASCADE)
- tasks.user_id → users.id (ON DELETE CASCADE)

**Rationale**: CASCADE ensures data consistency. Deleting a user removes all their conversations, messages, and tasks.

### Unique Constraints

- users.email (UNIQUE)
- messages(conversation_id, sequence_number) (UNIQUE)

### Check Constraints

- messages.role IN ('user', 'assistant')
- tasks.status IN ('pending', 'completed')

## Query Patterns

### Load Conversation History

```sql
SELECT m.*
FROM messages m
WHERE m.conversation_id = :conversation_id
ORDER BY m.sequence_number ASC;
```

**Expected Performance**: <100ms for 100 messages (indexed on conversation_id)

### Load User's Most Recent Conversation

```sql
SELECT c.*
FROM conversations c
WHERE c.user_id = :user_id
ORDER BY c.updated_at DESC
LIMIT 1;
```

**Expected Performance**: <50ms (indexed on user_id and updated_at)

### List User's Tasks (Filtered by Status)

```sql
SELECT t.*
FROM tasks t
WHERE t.user_id = :user_id
  AND t.status = :status  -- optional filter
ORDER BY t.created_at DESC;
```

**Expected Performance**: <100ms for 1000 tasks (indexed on user_id and status)

### Find Task by Title (Fuzzy Match)

```sql
SELECT t.*
FROM tasks t
WHERE t.user_id = :user_id
  AND LOWER(t.title) LIKE LOWER(:search_term)
ORDER BY t.created_at DESC;
```

**Expected Performance**: <200ms for 1000 tasks (full table scan on user's tasks, acceptable for MVP)

## Migration Strategy

### Initial Schema Creation

```sql
-- Run via SQLModel create_all() or Alembic migration

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    sequence_number INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (conversation_id, sequence_number)
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

### Future Schema Evolution

Use Alembic for migrations:
- Version control schema changes
- Rollback capability
- Data migration scripts

## Data Validation

### At Application Layer (SQLModel)

- Email format validation
- Password strength requirements (Better Auth handles)
- Title length limits (500 chars)
- Enum validation (role, status)

### At Database Layer

- NOT NULL constraints
- UNIQUE constraints
- FOREIGN KEY constraints
- CHECK constraints

## Performance Considerations

### Expected Data Volume (1 year)

- Users: 1,000
- Tasks per user: 100 (avg) → 100,000 tasks total
- Conversations per user: 1 (MVP) → 1,000 conversations total
- Messages per conversation: 100 (avg) → 100,000 messages total

### Index Strategy

- B-tree indexes on foreign keys (user_id, conversation_id)
- B-tree indexes on timestamps (created_at, updated_at)
- JSONB GIN index on tool_calls (if querying tool invocations)

### Query Optimization

- Limit result sets (pagination for large lists)
- Eager loading with relationships (avoid N+1 queries)
- Connection pooling (10-20 connections)

## Security Considerations

### User Isolation

- **CRITICAL**: All queries MUST filter by user_id
- Never allow user_id to be client-provided (extract from JWT)
- MCP tools enforce user_id filtering at tool level

### Data Encryption

- Passwords: Bcrypt/Argon2 hashing
- Database: TLS connections to Neon PostgreSQL
- At-rest: Neon handles encryption automatically

### Audit Trail

- tool_calls JSONB records all MCP tool invocations
- created_at/updated_at timestamps on all entities
- No soft deletes in MVP (hard deletes with CASCADE)

## Testing Data

### Seed Data for Development

```python
# Create test user
test_user = User(
    id="test-user-uuid",
    email="test@example.com",
    password_hash="$2b$12$..." # "password123" hashed
)

# Create test conversation
test_conversation = Conversation(
    id="test-conversation-uuid",
    user_id="test-user-uuid",
    title="Test Todo Conversation"
)

# Create test messages
test_messages = [
    Message(
        conversation_id="test-conversation-uuid",
        role=MessageRole.USER,
        content="Add buy groceries",
        sequence_number=1
    ),
    Message(
        conversation_id="test-conversation-uuid",
        role=MessageRole.ASSISTANT,
        content="I've added 'buy groceries' to your task list",
        tool_calls={"calls": [{"tool": "add_task", ...}]},
        sequence_number=2
    )
]

# Create test tasks
test_task = Task(
    user_id="test-user-uuid",
    title="buy groceries",
    status=TaskStatus.PENDING
)
```

## Next Steps

1. Implement SQLModel schemas in `backend/src/models/`
2. Create Alembic migration for initial schema
3. Implement database operations in `backend/src/db/operations.py`
4. Write unit tests for CRUD operations
5. Generate API contracts using this data model
