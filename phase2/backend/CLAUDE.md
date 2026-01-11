# Backend CLAUDE.md – FastAPI Development Guide

**Project**: Hackathon II – Phase II
**Framework**: FastAPI 0.110+
**Language**: Python 3.10+
**ORM**: SQLModel 0.0.14+
**Status**: Implementation Ready

---

## Overview

The Phase II backend is a FastAPI application with:
- **Authentication**: JWT validation middleware, Better Auth integration
- **Database**: PostgreSQL with SQLModel ORM
- **API**: RESTful endpoints with user isolation
- **Services**: Business logic layer with user-scoped queries
- **Security**: JWT verification, user_id matching, query filtering

---

## File Structure

```
backend/
├── CLAUDE.md                          # This file
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Project metadata
├── .env.example
├── main.py                            # FastAPI app entry
└── src/
    ├── config.py                      # T005: Environment config loading
    │
    ├── db/
    │   ├── database.py                # T006: Database connection
    │   └── models.py                  # T007: SQLModel definitions
    │
    ├── models/
    │   ├── user.py                    # T011: User model
    │   └── task.py                    # T012: Task model
    │
    ├── schemas/
    │   ├── user.py                    # T013: User Pydantic schemas
    │   └── task.py                    # T014: Task Pydantic schemas
    │
    ├── middleware/
    │   └── auth.py                    # T008: JWT validation
    │
    ├── services/
    │   └── task_service.py            # T015, T024: Task business logic
    │
    └── api/
        └── routes/
            ├── auth.py                # Auth endpoints (signup/login/logout)
            └── tasks.py               # T018-T023: Task CRUD endpoints
```

---

## Environment Variables

**File**: `.env.example`

```env
# Database
DATABASE_URL=postgresql://user:password@neon.tech/dbname

# JWT
JWT_SECRET=your-secret-key-here-min-32-chars

# Better Auth
BETTER_AUTH_SECRET=your-better-auth-secret

# Server
DEBUG=False
PORT=8000
```

**Loading in Code**:
```python
from src.config import settings

database_url = settings.DATABASE_URL
jwt_secret = settings.JWT_SECRET
```

---

## Key Patterns

### 1. Configuration Management (T005)

**File**: `src/config.py`

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    PORT: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. Database Connection (T006)

**File**: `src/db/database.py`

```python
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
from src.config import settings
from typing import Generator

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    connect_args={"sslmode": "require"},  # For Neon PostgreSQL
    poolclass=NullPool if "neon" in settings.DATABASE_URL else None,
)

def create_db_and_tables():
    """Create all tables on startup"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for route handlers to get DB session"""
    with Session(engine) as session:
        yield session
```

### 3. SQLModel Definitions (T007)

**File**: `src/db/models.py`

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    status: str = Field(default="incomplete")  # incomplete | complete
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

### 4. JWT Middleware (T008)

**File**: `src/middleware/auth.py`

```python
import jwt
from jwt import PyJWTError
from fastapi import Request, HTTPException, status
from src.config import settings
from typing import Optional

def extract_token(request: Request) -> Optional[str]:
    """Extract JWT from Authorization header"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:]

def verify_token(token: str) -> dict:
    """Verify JWT signature and extract claims"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

async def auth_middleware(request: Request, call_next):
    """Middleware to validate JWT on protected routes"""
    # Skip auth for public endpoints
    public_paths = ["/auth/signup", "/auth/login", "/docs", "/openapi.json"]
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Extract and verify token
    token = extract_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token"
        )

    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims"
        )

    # Verify route user_id matches JWT user_id
    route_user_id = request.path_params.get("user_id")
    if route_user_id and route_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Attach user_id to request state
    request.state.user_id = user_id
    response = await call_next(request)
    return response
```

### 5. Pydantic Schemas (T013, T014)

**File**: `src/schemas/task.py`

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)

    @field_validator("title")
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("description")
    def description_trimmed(cls, v):
        return v.strip() if v else v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)

    @field_validator("title")
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

class TaskRead(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    status: str  # incomplete | complete
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### 6. Task Service (T015, T024)

**File**: `src/services/task_service.py`

```python
from sqlmodel import Session, select, func
from src.db.models import Task
from src.schemas.task import TaskCreate, TaskUpdate
from datetime import datetime
from typing import Optional, List

class TaskService:
    @staticmethod
    def create_task(
        session: Session,
        user_id: str,
        task_data: TaskCreate
    ) -> Task:
        """Create a new task for user"""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            status="incomplete"
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_user_tasks(
        session: Session,
        user_id: str,
        status: Optional[str] = None
    ) -> List[Task]:
        """Get all tasks for user, optionally filtered by status"""
        query = select(Task).where(Task.user_id == user_id)

        if status:
            query = query.where(Task.status == status)

        query = query.order_by(Task.created_at.desc())
        return session.exec(query).all()

    @staticmethod
    def get_task(
        session: Session,
        task_id: int,
        user_id: str
    ) -> Optional[Task]:
        """Get single task, verifying ownership"""
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        return session.exec(query).first()

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        user_id: str,
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """Update task, verifying ownership"""
        task = TaskService.get_task(session, task_id, user_id)
        if not task:
            return None

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(
        session: Session,
        task_id: int,
        user_id: str
    ) -> bool:
        """Delete task, verifying ownership"""
        task = TaskService.get_task(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_status(
        session: Session,
        task_id: int,
        user_id: str
    ) -> Optional[Task]:
        """Toggle task completion status"""
        task = TaskService.get_task(session, task_id, user_id)
        if not task:
            return None

        task.status = "complete" if task.status == "incomplete" else "incomplete"
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
```

### 7. API Routes - Tasks (T018-T023)

**File**: `src/api/routes/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from src.db.database import get_session
from src.db.models import Task
from src.services.task_service import TaskService
from src.schemas.task import TaskCreate, TaskUpdate, TaskRead
from typing import List, Optional
from requests import Request

router = APIRouter(prefix="/api/users", tags=["tasks"])

@router.post("/{user_id}/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    request: Request,
    session: Session = Depends(get_session)
):
    """T018: Create a new task"""
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    task = TaskService.create_task(session, user_id, task_data)
    return {
        "success": True,
        "data": TaskRead.from_orm(task)
    }

@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    status: Optional[str] = Query(None),
    request: Request = None,
    session: Session = Depends(get_session)
):
    """T019: List user's tasks"""
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    tasks = TaskService.get_user_tasks(session, user_id, status)
    return {
        "success": True,
        "data": [TaskRead.from_orm(task) for task in tasks]
    }

@router.get("/{user_id}/tasks/{id}")
async def get_task(
    user_id: str,
    id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """T020: Get single task"""
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    task = TaskService.get_task(session, id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": TaskRead.from_orm(task)
    }

@router.put("/{user_id}/tasks/{id}")
async def update_task(
    user_id: str,
    id: int,
    task_data: TaskUpdate,
    request: Request,
    session: Session = Depends(get_session)
):
    """T021: Update task"""
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    task = TaskService.update_task(session, id, user_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": TaskRead.from_orm(task)
    }

@router.delete("/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """T022: Delete task"""
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    success = TaskService.delete_task(session, id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return None

@router.patch("/{user_id}/tasks/{id}/complete")
async def toggle_task(
    user_id: str,
    id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """T023: Toggle task completion status"""
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    task = TaskService.toggle_task_status(session, id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": TaskRead.from_orm(task)
    }
```

### 8. Main FastAPI App

**File**: `main.py`

```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config import settings
from src.db.database import create_db_and_tables, get_session
from src.middleware.auth import auth_middleware
from src.api.routes import tasks, auth  # Import route modules

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    create_db_and_tables()
    print("Database tables created")
    yield
    # Shutdown
    print("Application shutting down")

app = FastAPI(
    title="Phase II Todo API",
    description="Full-stack Todo application",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware for JWT validation
@app.middleware("http")
async def auth_check(request, call_next):
    return await auth_middleware(request, call_next)

# Include routers
app.include_router(auth.router)  # /auth/signup, /auth/login, /auth/logout
app.include_router(tasks.router)  # /api/users/{user_id}/tasks/*

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )
```

---

## Development Rules

### 1. User Isolation in Queries
**CRITICAL**: Every query must filter by `user_id`

```python
# ✅ CORRECT - Filters by user_id
query = select(Task).where(Task.user_id == user_id)

# ❌ INCORRECT - No user filter (SECURITY RISK!)
query = select(Task)
```

### 2. Error Handling Standard
All endpoints must return consistent error format:

```python
{
  "success": false,
  "error": "error_code",
  "message": "User-friendly message"
}
```

### 3. HTTP Status Codes
Use correct status codes:
- `200`: GET, PUT, PATCH success
- `201`: POST success (created)
- `204`: DELETE success (no content)
- `400`: Validation error
- `401`: Missing/invalid JWT
- `403`: User ID mismatch
- `404`: Resource not found
- `500`: Server error

### 4. JWT Verification
- Always verify token signature
- Always check expiration
- Always extract user_id from `sub` claim
- Always match route user_id with JWT user_id

```python
if user_id != request.state.user_id:
    raise HTTPException(status_code=403, detail="Access denied")
```

### 5. SQLModel Queries
Use SQLModel `select()` syntax (not SQLAlchemy raw queries):

```python
from sqlmodel import select

# ✅ CORRECT
query = select(Task).where(Task.user_id == user_id)
tasks = session.exec(query).all()

# ❌ INCORRECT (raw SQL syntax)
tasks = session.query(Task).filter(Task.user_id == user_id).all()
```

### 6. Dependency Injection
Use FastAPI dependencies for DB session:

```python
from fastapi import Depends
from src.db.database import get_session

@router.get("/tasks")
async def get_tasks(session: Session = Depends(get_session)):
    # session is automatically provided
    tasks = TaskService.get_tasks(session, user_id)
    return {"data": tasks}
```

### 7. Service Layer Pattern
- Routes: Handle HTTP, verify user_id, call services
- Services: Contain business logic, query database
- Models: Define data structure

```
Route Handler
    ↓
Service Method
    ↓
Database Query
```

### 8. Validation
Validate at boundaries (user input):

```python
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)

    @field_validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
```

---

## Database Operations

### Create
```python
task = Task(user_id=user_id, title="Buy milk", status="incomplete")
session.add(task)
session.commit()
session.refresh(task)
```

### Read
```python
# Single task
task = session.exec(
    select(Task).where(Task.id == 1, Task.user_id == user_id)
).first()

# List tasks
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()
```

### Update
```python
task.title = "New title"
task.updated_at = datetime.utcnow()
session.add(task)
session.commit()
session.refresh(task)
```

### Delete
```python
session.delete(task)
session.commit()
```

---

## Testing Checklist

Before completing backend implementation:

- [ ] POST /auth/signup creates user in Better Auth
- [ ] POST /auth/login returns JWT token
- [ ] POST /api/{user_id}/tasks requires JWT
- [ ] POST /api/{user_id}/tasks creates task with user_id
- [ ] GET /api/{user_id}/tasks returns only authenticated user's tasks
- [ ] GET /api/{user_id}/tasks/{id} returns 404 for other user's task
- [ ] PUT /api/{user_id}/tasks/{id} returns 403 for other user's task
- [ ] DELETE /api/{user_id}/tasks/{id} returns 403 for other user's task
- [ ] PATCH /api/{user_id}/tasks/{id}/complete toggles status
- [ ] Missing JWT returns 401
- [ ] Expired JWT returns 401
- [ ] URL user_id != JWT user_id returns 403
- [ ] Invalid requests return 400 with validation errors

---

## Environment & Dependencies

### requirements.txt
```
fastapi==0.110.0
uvicorn==0.27.0
sqlmodel==0.0.14
pydantic-settings==2.1.0
python-better-auth==latest
pyjwt==2.8.0
python-dotenv==1.0.0
sqlalchemy==2.0.0
```

### Run Server
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run development server
python main.py

# API will be at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## Key Points to Remember

1. **Always filter by user_id**: Every query includes WHERE user_id = ?
2. **Verify route user_id**: Compare against request.state.user_id from JWT
3. **Use service layer**: Don't put query logic in route handlers
4. **Consistent response format**: { success: bool, data?: any, error?: string }
5. **Proper HTTP status codes**: Use 201 for POST, 204 for DELETE, 403 for access denied
6. **JWT from middleware**: request.state.user_id is already verified
7. **No hardcoded secrets**: All config in environment variables

---

**Last Updated**: January 4, 2026
**Ready for**: Tasks T004-T024 (Setup, Foundation, Services, Routes)
