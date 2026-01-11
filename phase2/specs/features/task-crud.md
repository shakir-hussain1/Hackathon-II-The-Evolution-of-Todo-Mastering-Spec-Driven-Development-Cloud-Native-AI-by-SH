# Feature: Task CRUD Operations

**Feature ID**: TASK-001
**Status**: Specification
**Related Spec**: @specs/overview.md

---

## Overview

Task CRUD (Create, Read, Update, Delete) operations enable users to manage their todo items. All operations require authentication and are scoped to the authenticated user.

---

## Requirements

### REQ-TASK-001: Create Task
- Endpoint: `POST /api/users/{user_id}/tasks`
- Required: `title` (string, max 255 chars, not empty)
- Optional: `description` (string, max 10000 chars)
- Returns: Task object with id, status, created_at, updated_at
- Status: 201 Created
- Errors: 400 (validation), 401 (unauthorized), 403 (user_id mismatch)

### REQ-TASK-002: Read Task List
- Endpoint: `GET /api/users/{user_id}/tasks`
- Query: Optional `status` filter (incomplete/complete)
- Returns: Array of task objects
- Status: 200 OK
- Errors: 401 (unauthorized), 403 (user_id mismatch)

### REQ-TASK-003: Read Single Task
- Endpoint: `GET /api/users/{user_id}/tasks/{id}`
- Returns: Single task object with all fields
- Status: 200 OK
- Errors: 401 (unauthorized), 403 (user_id mismatch), 404 (not found)

### REQ-TASK-004: Update Task
- Endpoint: `PUT /api/users/{user_id}/tasks/{id}`
- Optional: `title` (updated title)
- Optional: `description` (updated description)
- Returns: Updated task object
- Status: 200 OK
- Errors: 400 (validation), 401 (unauthorized), 403 (user_id mismatch), 404 (not found)

### REQ-TASK-005: Delete Task
- Endpoint: `DELETE /api/users/{user_id}/tasks/{id}`
- Returns: Empty response
- Status: 204 No Content
- Errors: 401 (unauthorized), 403 (user_id mismatch), 404 (not found)

### REQ-TASK-006: Toggle Task Completion
- Endpoint: `PATCH /api/users/{user_id}/tasks/{id}/complete`
- Behavior: Flips status between "incomplete" and "complete"
- Returns: Updated task with new status
- Status: 200 OK
- Errors: 401 (unauthorized), 403 (user_id mismatch), 404 (not found)

---

## Data Model

### Task Entity
```
{
  "id": integer (auto-increment),
  "user_id": string (UUID, required),
  "title": string (required, max 255),
  "description": string (optional, max 10000),
  "status": enum ("incomplete" | "complete", default "incomplete"),
  "created_at": timestamp (auto-set),
  "updated_at": timestamp (auto-updated)
}
```

### Task Create Request
```json
{
  "title": "Buy groceries",
  "description": "Fresh vegetables and milk"
}
```

### Task Response
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Fresh vegetables and milk",
  "status": "incomplete",
  "created_at": "2026-01-04T10:00:00Z",
  "updated_at": "2026-01-04T10:00:00Z"
}
```

---

## Validation Rules

### Title Validation
- Required (not empty)
- Max 255 characters
- Whitespace trimmed
- No special restrictions

### Description Validation
- Optional (can be null)
- Max 10000 characters
- Whitespace trimmed

### Status Validation
- Only: "incomplete" or "complete"
- Default: "incomplete" on creation
- Cannot be set manually (use toggle endpoint)

---

## User Isolation

Every operation scoped to authenticated user:

1. **Create**: Task created with authenticated user_id
2. **Read**: Only authenticated user's tasks returned
3. **Update**: Only if task belongs to authenticated user
4. **Delete**: Only if task belongs to authenticated user
5. **Toggle**: Only if task belongs to authenticated user

**Enforcement**:
- Database query includes: `WHERE user_id = authenticated_user_id`
- URL `user_id` verified against JWT `user_id`
- Mismatch → 403 Forbidden

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Title cannot be empty"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": "unauthorized",
  "message": "Missing or invalid authentication"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": "forbidden",
  "message": "You do not have permission to access this task"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "not_found",
  "message": "Task not found"
}
```

---

## Implementation Checklist

- [ ] POST /api/{user_id}/tasks implemented
- [ ] GET /api/{user_id}/tasks implemented
- [ ] GET /api/{user_id}/tasks/{id} implemented
- [ ] PUT /api/{user_id}/tasks/{id} implemented
- [ ] DELETE /api/{user_id}/tasks/{id} implemented
- [ ] PATCH /api/{user_id}/tasks/{id}/complete implemented
- [ ] All endpoints require JWT
- [ ] All endpoints verify user_id
- [ ] Database queries filtered by user_id
- [ ] Validation rules enforced
- [ ] Error responses JSON format

---

**Status**: Ready for Implementation
