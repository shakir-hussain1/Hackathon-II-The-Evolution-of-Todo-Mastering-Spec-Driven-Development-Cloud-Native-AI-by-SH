# API Contract: REST Endpoints

**Feature ID**: TASK-001, AUTH-001
**Status**: Specification
**Related Specs**: @specs/features/task-crud.md, @specs/features/authentication.md

---

## Overview

All API endpoints follow RESTful conventions with JSON request/response bodies. Every endpoint (except /auth/signup and /auth/login) requires a valid JWT token in the Authorization header and is scoped to the authenticated user.

---

## Authentication Endpoints

### POST /auth/signup

**Purpose**: Register a new user and issue JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "user": {
    "id": "user-uuid-123",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errors**:
- 400 Bad Request: Invalid email format, password too short, user already exists
- 500 Internal Server Error: Database error

**Implementation**: Better Auth handles signup logic

---

### POST /auth/login

**Purpose**: Authenticate user and issue JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "user": {
    "id": "user-uuid-123",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errors**:
- 400 Bad Request: Missing email or password
- 401 Unauthorized: Invalid credentials
- 500 Internal Server Error: Database error

**Implementation**: Better Auth handles login logic

---

### POST /auth/logout

**Purpose**: Invalidate session (frontend removes token)

**Request**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Errors**:
- 401 Unauthorized: Missing or invalid token

**Implementation**: Backend acknowledges logout, frontend removes JWT from storage

---

## Task CRUD Endpoints

### POST /api/users/{user_id}/tasks

**Purpose**: Create a new task for the authenticated user

**Path Parameters**:
- `user_id`: User UUID from JWT token (must match authenticated user)

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Fresh vegetables and milk (optional)"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user-uuid-123",
    "title": "Buy groceries",
    "description": "Fresh vegetables and milk",
    "status": "incomplete",
    "created_at": "2026-01-04T10:00:00Z",
    "updated_at": "2026-01-04T10:00:00Z"
  }
}
```

**Validation**:
- `title`: Required, max 255 chars, no empty strings
- `description`: Optional, max 10000 chars

**Errors**:
- 400 Bad Request: Title empty, title > 255 chars, description > 10000 chars
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: URL user_id != JWT user_id
- 500 Internal Server Error: Database error

**Database Action**:
```sql
INSERT INTO tasks (user_id, title, description, status, created_at, updated_at)
VALUES (?, ?, ?, 'incomplete', NOW(), NOW())
```

---

### GET /api/users/{user_id}/tasks

**Purpose**: List all tasks for the authenticated user

**Path Parameters**:
- `user_id`: User UUID from JWT token (must match authenticated user)

**Request Headers**:
```
Authorization: Bearer <token>
```

**Query Parameters** (optional):
- `status`: Filter by "incomplete" or "complete"

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": "user-uuid-123",
      "title": "Buy groceries",
      "description": "Fresh vegetables",
      "status": "incomplete",
      "created_at": "2026-01-04T10:00:00Z",
      "updated_at": "2026-01-04T10:00:00Z"
    },
    {
      "id": 2,
      "user_id": "user-uuid-123",
      "title": "Call dentist",
      "description": null,
      "status": "complete",
      "created_at": "2026-01-04T11:00:00Z",
      "updated_at": "2026-01-04T11:30:00Z"
    }
  ]
}
```

**Database Query**:
```sql
SELECT * FROM tasks WHERE user_id = ? [AND status = ?]
ORDER BY created_at DESC
```

**Errors**:
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: URL user_id != JWT user_id
- 500 Internal Server Error: Database error

**Notes**:
- Empty array if no tasks
- Status filter optional
- Always ordered by most recently created first

---

### GET /api/users/{user_id}/tasks/{id}

**Purpose**: Retrieve a single task by ID

**Path Parameters**:
- `user_id`: User UUID from JWT token
- `id`: Task ID (integer)

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user-uuid-123",
    "title": "Buy groceries",
    "description": "Fresh vegetables and milk",
    "status": "incomplete",
    "created_at": "2026-01-04T10:00:00Z",
    "updated_at": "2026-01-04T10:00:00Z"
  }
}
```

**Database Query**:
```sql
SELECT * FROM tasks WHERE id = ? AND user_id = ?
```

**Errors**:
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: URL user_id != JWT user_id (or task belongs to different user)
- 404 Not Found: Task does not exist
- 500 Internal Server Error: Database error

---

### PUT /api/users/{user_id}/tasks/{id}

**Purpose**: Update task title and/or description

**Path Parameters**:
- `user_id`: User UUID from JWT token
- `id`: Task ID (integer)

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body** (at least one field required):
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user-uuid-123",
    "title": "Updated title",
    "description": "Updated description",
    "status": "incomplete",
    "created_at": "2026-01-04T10:00:00Z",
    "updated_at": "2026-01-04T10:30:00Z"
  }
}
```

**Validation**:
- `title`: Max 255 chars if provided
- `description`: Max 10000 chars if provided
- At least one field must be provided

**Database Update**:
```sql
UPDATE tasks
SET title = COALESCE(?, title),
    description = COALESCE(?, description),
    updated_at = NOW()
WHERE id = ? AND user_id = ?
```

**Errors**:
- 400 Bad Request: Title > 255 chars, description > 10000 chars, no fields provided
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: URL user_id != JWT user_id (or task belongs to different user)
- 404 Not Found: Task does not exist
- 500 Internal Server Error: Database error

**Notes**:
- Status cannot be updated via PUT (use PATCH endpoint)
- Only fields in request body are updated

---

### DELETE /api/users/{user_id}/tasks/{id}

**Purpose**: Permanently delete a task

**Path Parameters**:
- `user_id`: User UUID from JWT token
- `id`: Task ID (integer)

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response** (204 No Content):
```
(empty body)
```

**Database Query**:
```sql
DELETE FROM tasks WHERE id = ? AND user_id = ?
```

**Errors**:
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: URL user_id != JWT user_id (or task belongs to different user)
- 404 Not Found: Task does not exist
- 500 Internal Server Error: Database error

**Notes**:
- No response body on success
- Deletion is permanent and cannot be undone

---

### PATCH /api/users/{user_id}/tasks/{id}/complete

**Purpose**: Toggle task completion status

**Path Parameters**:
- `user_id`: User UUID from JWT token
- `id`: Task ID (integer)

**Request Headers**:
```
Authorization: Bearer <token>
```

**Request Body**: (empty)

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user-uuid-123",
    "title": "Buy groceries",
    "description": "Fresh vegetables and milk",
    "status": "complete",
    "created_at": "2026-01-04T10:00:00Z",
    "updated_at": "2026-01-04T10:45:00Z"
  }
}
```

**Toggle Logic**:
```python
new_status = "complete" if current_status == "incomplete" else "incomplete"
```

**Database Update**:
```sql
UPDATE tasks
SET status = CASE
      WHEN status = 'incomplete' THEN 'complete'
      WHEN status = 'complete' THEN 'incomplete'
    END,
    updated_at = NOW()
WHERE id = ? AND user_id = ?
```

**Errors**:
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: URL user_id != JWT user_id (or task belongs to different user)
- 404 Not Found: Task does not exist
- 500 Internal Server Error: Database error

---

## HTTP Status Codes

| Status | Use Case |
|--------|----------|
| **200 OK** | Successful GET, PUT, PATCH with data |
| **201 Created** | Successful POST (new resource) |
| **204 No Content** | Successful DELETE (no data) |
| **400 Bad Request** | Validation error (invalid input) |
| **401 Unauthorized** | Missing/invalid JWT token |
| **403 Forbidden** | user_id mismatch or no permission |
| **404 Not Found** | Resource doesn't exist |
| **500 Internal Server Error** | Unrecoverable server error |

---

## Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "error": "<error_code>",
  "message": "<user-friendly message>"
}
```

**Error Codes**:
- `validation_error`: Input validation failed
- `unauthorized`: Missing or invalid JWT
- `forbidden`: User lacks permission
- `not_found`: Resource doesn't exist
- `server_error`: Internal server error

---

## JWT Token Validation

Every endpoint (except /auth/signup and /auth/login) must:

1. Extract JWT from `Authorization: Bearer <token>` header
2. Verify JWT signature using `JWT_SECRET`
3. Check expiration (exp > current time)
4. Extract `sub` (user_id) from token
5. Verify route `user_id` matches JWT `sub`
6. Attach user_id to request context for handlers

**Middleware Pseudocode**:
```python
@app.middleware("http")
async def verify_jwt(request: Request, call_next):
    if request.url.path in ["/auth/signup", "/auth/login"]:
        return await call_next(request)

    # Extract token
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"success": False, "error": "unauthorized"}
        )

    token = auth_header[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        request.state.user_id = user_id
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"success": False})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"success": False})

    # Verify route user_id matches JWT user_id
    route_user_id = request.path_params.get("user_id")
    if route_user_id and route_user_id != user_id:
        return JSONResponse(status_code=403, content={"success": False})

    response = await call_next(request)
    return response
```

---

## Success Response Format

All successful responses follow this format:

```json
{
  "success": true,
  "data": <resource_or_array>
}
```

---

## Rate Limiting & Security

- No rate limiting in scope
- All tokens have 24-hour expiry
- Tokens never appear in query parameters (Authorization header only)
- No CORS in scope (Same-origin requests)

---

**Status**: Ready for Implementation
**Related**: @specs/features/task-crud.md, @specs/features/authentication.md
