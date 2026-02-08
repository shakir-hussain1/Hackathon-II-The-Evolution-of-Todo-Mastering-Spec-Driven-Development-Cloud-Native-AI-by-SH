# Data Model Design: Phase V – Advanced Cloud-Native Todo System

**Feature**: 001-cloud-native-kafka-dapr
**Created**: 2026-02-08
**Status**: Phase 1 Design

## Overview

This document defines the database schemas for all entities in Phase V. The system uses **PostgreSQL 15+** with separate schemas per service for logical isolation while sharing a single database instance (pragmatic MVP approach).

## Database Strategy

- **Single PostgreSQL Instance**: `phase5-todo-db`
- **Separate Schemas per Service**:
  - `chat_api` - Task entities and user data
  - `notification` - Notifications and reminders
  - `recurring_task` - Recurring task patterns
  - `audit` - Audit logs and event history
  - `websocket_sync` - WebSocket connection state (optional, can use Redis)

## Entities

### 1. User (Schema: `chat_api`)

**Table**: `chat_api.users`

```sql
CREATE TABLE chat_api.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    notification_preferences JSONB DEFAULT '{"email": true, "push": false}'::jsonb,
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    version INTEGER DEFAULT 1 NOT NULL
);

CREATE INDEX idx_users_email ON chat_api.users(email);
CREATE INDEX idx_users_deleted_at ON chat_api.users(deleted_at) WHERE deleted_at IS NULL;
```

**Fields**:
- `id`: UUID primary key
- `email`: Unique email address (indexed)
- `password_hash`: Bcrypt hashed password
- `full_name`: Display name
- `notification_preferences`: JSON object `{"email": boolean, "push": boolean}`
- `timezone`: IANA timezone (e.g., "America/New_York")
- `created_at`, `updated_at`: Timestamps
- `deleted_at`: Soft delete support
- `version`: Optimistic locking

---

### 2. Task (Schema: `chat_api`)

**Table**: `chat_api.tasks`

```sql
CREATE TABLE chat_api.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES chat_api.users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'archived')),
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('high', 'medium', 'low')),
    due_date TIMESTAMPTZ,
    tags TEXT[] DEFAULT '{}',
    recurrence_pattern JSONB,
    next_occurrence TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    version INTEGER DEFAULT 1 NOT NULL
);

CREATE INDEX idx_tasks_user_id ON chat_api.tasks(user_id);
CREATE INDEX idx_tasks_status ON chat_api.tasks(status);
CREATE INDEX idx_tasks_due_date ON chat_api.tasks(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_tasks_next_occurrence ON chat_api.tasks(next_occurrence) WHERE next_occurrence IS NOT NULL;
CREATE INDEX idx_tasks_tags ON chat_api.tasks USING GIN(tags);
CREATE INDEX idx_tasks_user_status ON chat_api.tasks(user_id, status);
CREATE INDEX idx_tasks_full_text ON chat_api.tasks USING GIN(to_tsvector('english', title || ' ' || COALESCE(description, '')));
```

**Fields**:
- `id`: UUID primary key
- `user_id`: Foreign key to users (indexed)
- `title`: Task title (max 200 chars, required)
- `description`: Optional detailed description
- `status`: Enum (`pending`, `completed`, `archived`)
- `priority`: Enum (`high`, `medium`, `low`)
- `due_date`: Optional deadline (indexed)
- `tags`: Array of strings (GIN indexed for fast search)
- `recurrence_pattern`: JSON object for recurring tasks (see below)
- `next_occurrence`: Computed next occurrence for recurring tasks (indexed)
- `completed_at`: Timestamp when marked complete
- `created_at`, `updated_at`, `deleted_at`: Timestamps
- `version`: Optimistic locking

**Recurrence Pattern Schema** (JSONB):
```json
{
  "frequency": "daily" | "weekly" | "monthly" | "yearly",
  "interval": 1,
  "days_of_week": [0, 1, 2, 3, 4, 5, 6],
  "day_of_month": 15,
  "end_date": "2026-12-31T23:59:59Z",
  "occurrences_count": 10
}
```

---

### 3. Reminder (Schema: `notification`)

**Table**: `notification.reminders`

```sql
CREATE TABLE notification.reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL,
    user_id UUID NOT NULL,
    scheduled_at TIMESTAMPTZ NOT NULL,
    sent_at TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed', 'cancelled')),
    channel VARCHAR(20) DEFAULT 'email' CHECK (channel IN ('email', 'push')),
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reminders_task_id ON notification.reminders(task_id);
CREATE INDEX idx_reminders_user_id ON notification.reminders(user_id);
CREATE INDEX idx_reminders_scheduled_at ON notification.reminders(scheduled_at);
CREATE INDEX idx_reminders_status ON notification.reminders(status) WHERE status = 'pending';
```

**Fields**:
- `id`: UUID primary key
- `task_id`: Reference to task (NOT FK - cross-schema, logical reference only)
- `user_id`: Reference to user
- `scheduled_at`: When to send reminder (indexed)
- `sent_at`: Actual send timestamp
- `status`: Enum (`pending`, `sent`, `failed`, `cancelled`)
- `channel`: Enum (`email`, `push`)
- `retry_count`: Number of retry attempts
- `error_message`: Error details if failed
- `created_at`, `updated_at`: Timestamps

---

### 4. Notification (Schema: `notification`)

**Table**: `notification.notifications`

```sql
CREATE TABLE notification.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    task_id UUID,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_id ON notification.notifications(user_id);
CREATE INDEX idx_notifications_read_at ON notification.notifications(read_at);
CREATE INDEX idx_notifications_created_at ON notification.notifications(created_at DESC);
```

**Fields**:
- `id`: UUID primary key
- `user_id`: Reference to user (indexed)
- `task_id`: Optional reference to task
- `type`: Notification type (e.g., `task_due`, `task_completed`, `reminder`)
- `title`: Short title
- `message`: Full notification message
- `read_at`: Timestamp when user read notification
- `created_at`: Timestamp

---

### 5. AuditLog (Schema: `audit`)

**Table**: `audit.audit_logs`

```sql
CREATE TABLE audit.audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id VARCHAR(100) UNIQUE NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_source VARCHAR(100) NOT NULL,
    user_id UUID,
    entity_type VARCHAR(50),
    entity_id UUID,
    operation VARCHAR(20) CHECK (operation IN ('create', 'update', 'delete', 'read')),
    changes JSONB,
    metadata JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_event_id ON audit.audit_logs(event_id);
CREATE INDEX idx_audit_logs_user_id ON audit.audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity ON audit.audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_timestamp ON audit.audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_event_type ON audit.audit_logs(event_type);
```

**Fields**:
- `id`: UUID primary key
- `event_id`: Unique Kafka event ID (indexed)
- `event_type`: CloudEvents type (e.g., `com.todo.task.created`)
- `event_source`: Service that generated event
- `user_id`: User who performed action
- `entity_type`: Type of entity (`task`, `user`, etc.)
- `entity_id`: UUID of entity
- `operation`: CRUD operation type
- `changes`: JSON object with before/after values
- `metadata`: Additional context (IP, user agent, etc.)
- `timestamp`: Event timestamp (indexed)
- `created_at`: Log entry created timestamp

---

### 6. RecurringTaskInstance (Schema: `recurring_task`)

**Table**: `recurring_task.recurring_instances`

```sql
CREATE TABLE recurring_task.recurring_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_task_id UUID NOT NULL,
    user_id UUID NOT NULL,
    scheduled_date TIMESTAMPTZ NOT NULL,
    created_task_id UUID,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'created', 'skipped', 'failed')),
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_recurring_instances_parent_task_id ON recurring_task.recurring_instances(parent_task_id);
CREATE INDEX idx_recurring_instances_scheduled_date ON recurring_task.recurring_instances(scheduled_date);
CREATE INDEX idx_recurring_instances_status ON recurring_task.recurring_instances(status) WHERE status = 'pending';
```

**Fields**:
- `id`: UUID primary key
- `parent_task_id`: Reference to original recurring task
- `user_id`: Task owner
- `scheduled_date`: When instance should be created (indexed)
- `created_task_id`: UUID of created task instance
- `status`: Enum (`pending`, `created`, `skipped`, `failed`)
- `error_message`: Error details if failed
- `created_at`, `updated_at`: Timestamps

---

### 7. WebSocketConnection (Schema: `websocket_sync`) - Optional

**Table**: `websocket_sync.connections`

```sql
CREATE TABLE websocket_sync.connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    connection_id VARCHAR(100) UNIQUE NOT NULL,
    connected_at TIMESTAMPTZ DEFAULT NOW(),
    last_ping TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_connections_user_id ON websocket_sync.connections(user_id);
CREATE INDEX idx_connections_last_ping ON websocket_sync.connections(last_ping);
```

**Alternative**: Use Redis for WebSocket connection state (faster, ephemeral)

---

## Migrations Strategy

**Tool**: Alembic (Python database migration tool)

**Migration Files**:
```
services/chat-api/alembic/versions/
├── 001_create_users_table.py
├── 002_create_tasks_table.py
├── 003_add_task_indexes.py
services/notification-service/alembic/versions/
├── 001_create_reminders_table.py
├── 002_create_notifications_table.py
services/recurring-task-service/alembic/versions/
├── 001_create_recurring_instances_table.py
services/audit-service/alembic/versions/
├── 001_create_audit_logs_table.py
```

**Initialization**:
```bash
# Run migrations for each service
cd services/chat-api && alembic upgrade head
cd services/notification-service && alembic upgrade head
cd services/recurring-task-service && alembic upgrade head
cd services/audit-service && alembic upgrade head
```

---

## Optimistic Locking Pattern

All mutable entities (`users`, `tasks`) include a `version` field for optimistic locking:

**Update Logic**:
```sql
UPDATE chat_api.tasks
SET title = $1, version = version + 1, updated_at = NOW()
WHERE id = $2 AND version = $3
RETURNING *;
```

If `RETURNING` clause returns 0 rows, another process modified the entity (version conflict).

**API Response**: `409 Conflict` with retry instructions.

---

## Data Retention Policies

- **Soft Deletes**: `users`, `tasks` use `deleted_at` field (never hard delete)
- **Audit Logs**: Retain for 90 days (configurable)
- **Notifications**: Retain for 30 days after read
- **Recurring Instances**: Clean up after 365 days

**Cleanup Job**: Kubernetes CronJob runs daily to purge old records.

---

## Schema Evolution

**Backward Compatibility**:
- Never drop columns (mark deprecated instead)
- Never change column types (add new column + migrate)
- Always use `ALTER TABLE ... ADD COLUMN ... DEFAULT` for new fields

**Testing**: All migrations tested in CI pipeline before deployment.

---

## Connection Pooling

**Configuration** (per service):
- **Pool Size**: 10 connections
- **Max Overflow**: 20 connections
- **Pool Timeout**: 30 seconds
- **Pool Recycle**: 3600 seconds (1 hour)

**SQLAlchemy Configuration**:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600
)
```

---

## Summary

This data model supports all Phase V functional requirements:

- ✅ **FR-001 to FR-010**: Advanced task features (recurring, due dates, priorities, tags, search)
- ✅ **FR-026 to FR-031**: Microservices with separate schemas
- ✅ **Event-Driven**: Audit logs capture all Kafka events
- ✅ **Optimistic Locking**: Version field prevents concurrent update conflicts
- ✅ **Full-Text Search**: GIN index on tasks for fast search
- ✅ **User Isolation**: All queries include `user_id` filter

**Next Steps**: Define API contracts (`contracts/`) and Dapr component specifications.
