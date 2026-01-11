# Database Schema Specification

**Feature ID**: TASK-001, AUTH-001
**Status**: Specification
**Database**: PostgreSQL 15+ (Neon)
**ORM**: SQLModel 0.0.14+

---

## Overview

The Phase II database contains two main tables:
- **users**: Managed by Better Auth (schema defined for reference)
- **tasks**: Custom table with user_id foreign key for ownership isolation

All queries filter by `user_id` to enforce multi-user isolation.

---

## Database Connection

**Connection String Format**:
```
postgresql://user:password@host:port/database_name
```

**Environment Variable**:
```
DATABASE_URL=postgresql://user:password@neon.tech/dbname
```

**SQLModel Connection**:
```python
from sqlmodel import SQLModel, create_engine, Session

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

---

## User Table

**Table Name**: `users`

**ORM Model** (`backend/src/models/user.py`):
```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Fields**:
- `id` (UUID string): Primary key, auto-generated
- `email` (string, unique, indexed): User's email address
- `password_hash` (string): Hashed password (Better Auth managed)
- `created_at` (timestamp, indexed): Account creation time
- `updated_at` (timestamp): Last update time

**Indexes**:
- `PK (id)`
- `UNIQUE (email)`
- `INDEX (created_at)` - for sorting users by signup date

**Constraints**:
- Primary key: `id`
- Unique: `email`
- Not null: `id`, `email`, `password_hash`

**Notes**:
- Managed by Better Auth authentication service
- Not directly created by Phase II code
- Referenced by tasks table via foreign key

---

## Tasks Table

**Table Name**: `tasks`

**ORM Model** (`backend/src/models/task.py`):
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255, index=False)
    description: Optional[str] = Field(default=None, max_length=10000)
    status: TaskStatus = Field(default=TaskStatus.INCOMPLETE)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional)
    user: Optional["User"] = Relationship(back_populates="tasks")
```

**SQL Definition**:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(10000),
    status VARCHAR(50) NOT NULL DEFAULT 'incomplete' CHECK (status IN ('incomplete', 'complete')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_tasks_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Field Definitions

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| `id` | SERIAL INT | PRIMARY KEY, AUTO INCREMENT | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEXED | Ownership & multi-user isolation |
| `title` | VARCHAR(255) | NOT NULL | Task title |
| `description` | VARCHAR(10000) | NULL | Optional task details |
| `status` | ENUM ('incomplete', 'complete') | NOT NULL, DEFAULT 'incomplete' | Task completion state |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW(), INDEXED | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Indexes

```sql
-- Primary Key
CREATE INDEX idx_tasks_id ON tasks(id);

-- Foreign Key (user_id) - enables fast filtering by user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Sorting by creation time
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Combined index for user-filtered sorting (optional performance)
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at);
```

### Constraints

```sql
-- Primary Key
ALTER TABLE tasks ADD CONSTRAINT pk_tasks PRIMARY KEY (id);

-- Foreign Key with CASCADE delete (delete tasks if user deleted)
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- Status enum check
ALTER TABLE tasks ADD CONSTRAINT chk_tasks_status
    CHECK (status IN ('incomplete', 'complete'));

-- Title not empty
ALTER TABLE tasks ADD CONSTRAINT chk_tasks_title_not_empty
    CHECK (title != '');

-- Max lengths enforced by application (VARCHAR already enforces)
```

---

## Query Patterns

### Create Task
```python
# Method 1: Using SQLModel
task = Task(
    user_id=authenticated_user_id,
    title="Buy groceries",
    description="Fresh vegetables",
    status=TaskStatus.INCOMPLETE
)
session.add(task)
session.commit()
session.refresh(task)
return task

# SQL Equivalent
INSERT INTO tasks (user_id, title, description, status, created_at, updated_at)
VALUES (?, ?, ?, 'incomplete', NOW(), NOW())
RETURNING *
```

### Read All User's Tasks
```python
# Method 1: Using SQLModel
tasks = session.query(Task).filter(
    Task.user_id == authenticated_user_id
).order_by(Task.created_at.desc()).all()

# SQL Equivalent
SELECT * FROM tasks WHERE user_id = ?
ORDER BY created_at DESC
```

### Read Single Task with User Verification
```python
# Method 1: Using SQLModel
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == authenticated_user_id
).first()

if not task:
    raise 404 Not Found

# SQL Equivalent
SELECT * FROM tasks WHERE id = ? AND user_id = ?
```

### Update Task
```python
# Method 1: Using SQLModel
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == authenticated_user_id
).first()

if not task:
    raise 404

task.title = new_title
task.description = new_description
task.updated_at = datetime.utcnow()
session.add(task)
session.commit()
session.refresh(task)
return task

# SQL Equivalent
UPDATE tasks
SET title = ?, description = ?, updated_at = NOW()
WHERE id = ? AND user_id = ?
RETURNING *
```

### Delete Task
```python
# Method 1: Using SQLModel
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == authenticated_user_id
).first()

if not task:
    raise 404

session.delete(task)
session.commit()

# SQL Equivalent
DELETE FROM tasks WHERE id = ? AND user_id = ?
```

### Toggle Task Status
```python
# Method 1: Using SQLModel
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == authenticated_user_id
).first()

if not task:
    raise 404

task.status = TaskStatus.COMPLETE if task.status == TaskStatus.INCOMPLETE else TaskStatus.INCOMPLETE
task.updated_at = datetime.utcnow()
session.add(task)
session.commit()
session.refresh(task)
return task

# SQL Equivalent
UPDATE tasks
SET status = CASE
      WHEN status = 'incomplete' THEN 'complete'
      WHEN status = 'complete' THEN 'incomplete'
    END,
    updated_at = NOW()
WHERE id = ? AND user_id = ?
RETURNING *
```

### List with Status Filter
```python
# Method 1: Using SQLModel
query = session.query(Task).filter(Task.user_id == authenticated_user_id)

if status:
    query = query.filter(Task.status == status)

tasks = query.order_by(Task.created_at.desc()).all()

# SQL Equivalent
SELECT * FROM tasks WHERE user_id = ? [AND status = ?]
ORDER BY created_at DESC
```

---

## Pydantic Schemas

### Task Create Schema (`backend/src/schemas/task.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Fresh vegetables and milk"
            }
        }
```

### Task Update Schema

```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated title",
                "description": "Updated description"
            }
        }

    @validator("title")
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v
```

### Task Read Schema

```python
from datetime import datetime
from enum import Enum

class TaskStatusEnum(str, Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

class TaskRead(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    status: TaskStatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user-123",
                "title": "Buy groceries",
                "description": "Fresh vegetables",
                "status": "incomplete",
                "created_at": "2026-01-04T10:00:00Z",
                "updated_at": "2026-01-04T10:00:00Z"
            }
        }
```

---

## Migration & Initialization

### Create Tables on Startup

```python
# backend/src/db/database.py
from sqlmodel import SQLModel, create_engine, Session
from backend.src.models.user import User
from backend.src.models.task import Task

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"sslmode": "require"}  # For Neon PostgreSQL
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### Initial Data (Optional)

No seeding data in scope. Each user creates their own tasks.

---

## Performance Considerations

1. **Index on user_id**: All queries filter by user_id for isolation
2. **Index on created_at**: For sorting tasks chronologically
3. **Combined index (user_id, created_at)**: Optional for WHERE + ORDER BY efficiency
4. **No N+1 queries**: Use eager loading if joining with users table
5. **Connection pooling**: SQLModel/SQLAlchemy handles via engine

---

## Data Integrity Rules

1. **Referential Integrity**: Tasks.user_id must exist in users.id
2. **Cascade Delete**: If user deleted, all their tasks deleted automatically
3. **Status Enum**: Only 'incomplete' or 'complete' allowed
4. **Title Required**: Cannot create task without title
5. **Title Max 255**: Enforced by VARCHAR(255) and Pydantic validation
6. **Description Max 10000**: Enforced by VARCHAR(10000) and validation

---

## User Isolation Queries

All queries must include `WHERE user_id = ?` to enforce isolation:

```python
# ✅ CORRECT - Filters by user_id
tasks = session.query(Task).filter(Task.user_id == user_id).all()

# ❌ INCORRECT - No user filter (allows cross-user access!)
tasks = session.query(Task).all()

# ✅ CORRECT - Update only user's task
session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id
).update({Task.title: new_title})

# ❌ INCORRECT - Updates any task with ID (security risk!)
session.query(Task).filter(Task.id == task_id).update({Task.title: new_title})
```

---

## Database Admin Commands

### Connect to Database

```bash
psql postgresql://user:password@host:port/dbname
```

### View Table Schema

```sql
\d tasks
\d users
```

### View All Tasks for a User

```sql
SELECT * FROM tasks WHERE user_id = 'user-uuid' ORDER BY created_at DESC;
```

### Count Tasks by User

```sql
SELECT user_id, COUNT(*) as task_count FROM tasks GROUP BY user_id;
```

### View Indexes

```sql
SELECT * FROM pg_indexes WHERE tablename = 'tasks';
```

---

**Status**: Ready for Implementation
**Related**: @specs/api/rest-endpoints.md, @specs/features/task-crud.md
