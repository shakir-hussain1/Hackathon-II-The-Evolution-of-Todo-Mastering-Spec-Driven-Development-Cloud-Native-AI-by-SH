# User Ownership Enforcement Skill - Specification

## Skill Overview
**Name:** user-ownership-enforcement
**Type:** Security Validation Skill
**Category:** Data Access Control

## Purpose
Ensures strict data ownership and isolation by validating that all database queries are properly filtered by authenticated user ID, preventing cross-user data access vulnerabilities.

## Input Requirements
- Database query code
- API endpoint handlers
- Route definitions
- Authentication middleware
- ORM/SQLModel models

## Core Functions

### 1. Query Filtering Validation
- Verify all queries include user_id filter
- Check WHERE clauses for user isolation
- Validate ORM query filters
- Ensure joins respect ownership

### 2. Route Parameter Validation
- Verify route user_id matches JWT user_id
- Check path parameters against auth
- Validate query parameters
- Ensure request body user_id consistency

### 3. CRUD Operation Validation
- **CREATE:** Verify user_id is set from JWT
- **READ:** Ensure user_id filter on queries
- **UPDATE:** Validate ownership before modification
- **DELETE:** Confirm ownership before deletion

### 4. Cross-User Access Prevention
- Detect IDOR vulnerabilities
- Identify missing ownership checks
- Flag admin bypass opportunities
- Check for privilege escalation

### 5. Data Isolation Verification
- Validate user cannot access others' data
- Ensure list endpoints filter by user
- Check detail endpoints validate ownership
- Verify cascade operations respect boundaries

## Validation Rules

### Query Filtering Standards
```python
# REQUIRED: Every user-scoped query MUST filter by user_id

# ✓ CORRECT
todos = session.exec(
    select(Todo).where(Todo.user_id == current_user.id)
).all()

# ✗ INCORRECT - Missing user_id filter
todos = session.exec(select(Todo)).all()  # Returns ALL users' todos

# ✗ INCORRECT - Using route param without validation
user_id = request.path_params["user_id"]
todos = session.exec(
    select(Todo).where(Todo.user_id == user_id)  # user_id not validated
).all()

# ✓ CORRECT - Route param validated against JWT
user_id = request.path_params["user_id"]
if user_id != current_user.id:
    raise HTTPException(403, "Access denied")
todos = session.exec(
    select(Todo).where(Todo.user_id == user_id)
).all()
```

### Route Parameter Standards
```python
# ✓ CORRECT - Extract user_id from JWT, ignore route params
@app.get("/users/{user_id}/todos")
def get_user_todos(user_id: int, current_user: User = Depends(get_current_user)):
    # Ignore route param, use JWT user_id
    todos = session.exec(
        select(Todo).where(Todo.user_id == current_user.id)
    ).all()
    return todos

# ✗ INCORRECT - Trusting route parameter
@app.get("/users/{user_id}/todos")
def get_user_todos(user_id: int):
    todos = session.exec(
        select(Todo).where(Todo.user_id == user_id)  # IDOR vulnerability
    ).all()
    return todos
```

### Ownership Validation Standards
```python
# ✓ CORRECT - Verify ownership before update/delete
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_user)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(404, "Todo not found")
    if todo.user_id != current_user.id:  # ✓ Ownership check
        raise HTTPException(403, "Access denied")
    session.delete(todo)
    session.commit()
    return {"ok": True}

# ✗ INCORRECT - No ownership check
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(404)
    session.delete(todo)  # ❌ Can delete anyone's todo
    session.commit()
    return {"ok": True}
```

## Validation Process

### Step 1: Endpoint Inventory
1. List all API endpoints
2. Categorize by operation (CRUD)
3. Identify user-scoped resources
4. Flag public vs. private endpoints

### Step 2: Query Analysis
1. Extract all database queries
2. Check for user_id filters
3. Verify JOIN conditions
4. Validate subqueries

### Step 3: Route Parameter Audit
1. Find all route parameters
2. Check user_id parameter usage
3. Verify JWT validation
4. Test parameter tampering

### Step 4: Ownership Verification
1. Test CREATE with different users
2. Test READ with cross-user IDs
3. Test UPDATE ownership checks
4. Test DELETE ownership enforcement

### Step 5: Penetration Testing
1. Attempt IDOR attacks
2. Try parameter manipulation
3. Test privilege escalation
4. Verify error messages don't leak data

## Output Format

### Ownership Enforcement Report
```markdown
## USER OWNERSHIP ENFORCEMENT REPORT

**Overall Status:** [SECURE | VULNERABLE | CRITICAL]
**Endpoints Analyzed:** 24
**Vulnerabilities Found:** 3

### Query Filtering Analysis
**Total User-Scoped Queries:** 18
**Properly Filtered:** 15 (83%)
**Missing Filters:** 3 (17%)

#### ✓ Properly Filtered Queries
- `GET /todos` - filters by current_user.id ✓
- `POST /todos` - sets user_id from JWT ✓
- `GET /todos/{id}` - validates ownership ✓

#### ✗ Missing User Filters (CRITICAL)
1. **GET /todos/search**
   - File: api/todos.py:45
   - Issue: Query missing user_id filter
   - Impact: Returns all users' todos
   - Fix: Add `.where(Todo.user_id == current_user.id)`

2. **DELETE /todos/{id}**
   - File: api/todos.py:89
   - Issue: No ownership check before delete
   - Impact: Can delete any user's todo
   - Fix: Validate `todo.user_id == current_user.id`

### Route Parameter Validation
**Total Route Parameters:** 8
**Validated Against JWT:** 5 (63%)
**IDOR Vulnerabilities:** 3

#### ✗ IDOR Vulnerabilities (HIGH)
1. **GET /users/{user_id}/profile**
   - File: api/users.py:23
   - Issue: Trusts route user_id parameter
   - Impact: Can view any user's profile
   - Fix: Use current_user.id instead of route param

### CRUD Operation Compliance
| Operation | Total | Compliant | Vulnerable | %     |
|-----------|-------|-----------|------------|-------|
| CREATE    | 6     | 6         | 0          | 100%  |
| READ      | 10    | 7         | 3          | 70%   |
| UPDATE    | 5     | 4         | 1          | 80%   |
| DELETE    | 3     | 2         | 1          | 67%   |
```

### Vulnerability Details
```markdown
## VULNERABILITIES

### CRITICAL: Insecure Object Direct Reference (IDOR)
**Endpoint:** GET /users/{user_id}/todos
**File:** api/todos.py:56
**Issue:** Route parameter user_id used without validation
**Proof of Concept:**
```http
GET /users/123/todos
Authorization: Bearer <user_456_token>
# Returns user 123's todos even though JWT is for user 456
```

**Impact:** Complete user data access breach
**CVSS Score:** 9.1 (Critical)
**CWE:** CWE-639 - Authorization Bypass Through User-Controlled Key

**Remediation:**
```python
# BEFORE (vulnerable)
@app.get("/users/{user_id}/todos")
def get_user_todos(user_id: int):
    return session.exec(select(Todo).where(Todo.user_id == user_id)).all()

# AFTER (secure)
@app.get("/users/{user_id}/todos")
def get_user_todos(user_id: int, current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(403, "Access denied")
    return session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
```
```

### Isolation Guarantee Confirmation
```markdown
## ISOLATION GUARANTEES

### ✓ CONFIRMED
- Users cannot list other users' todos
- Users cannot create todos for other users
- Admin endpoints properly separated

### ✗ NOT CONFIRMED (Requires Fix)
- Users CAN read other users' todo details (IDOR)
- Users CAN update other users' todos (Missing check)
- Users CAN delete other users' todos (Missing check)

**Verdict:** ISOLATION NOT GUARANTEED - Critical vulnerabilities present
```

## Common Vulnerability Patterns

### Pattern 1: Missing User Filter
```python
# ❌ VULNERABLE
def get_todos(session):
    return session.exec(select(Todo)).all()

# ✓ SECURE
def get_todos(session, user_id: int):
    return session.exec(
        select(Todo).where(Todo.user_id == user_id)
    ).all()
```

### Pattern 2: Trusting Route Parameters
```python
# ❌ VULNERABLE
@app.get("/todos/{id}")
def get_todo(id: int, user_id: int):  # user_id from query param
    return session.exec(
        select(Todo).where(Todo.id == id, Todo.user_id == user_id)
    ).first()

# ✓ SECURE
@app.get("/todos/{id}")
def get_todo(id: int, current_user: User = Depends(get_current_user)):
    todo = session.get(Todo, id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(404)
    return todo
```

### Pattern 3: Missing Ownership Check on Modification
```python
# ❌ VULNERABLE
@app.put("/todos/{id}")
def update_todo(id: int, data: TodoUpdate):
    todo = session.get(Todo, id)
    for key, value in data.dict().items():
        setattr(todo, key, value)
    session.commit()
    return todo

# ✓ SECURE
@app.put("/todos/{id}")
def update_todo(id: int, data: TodoUpdate, current_user: User = Depends(get_current_user)):
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(404)
    if todo.user_id != current_user.id:  # ✓ Ownership check
        raise HTTPException(403, "Access denied")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    session.commit()
    return todo
```

## Integration Points

### Works With
- auth-security-validator agent
- jwt-verification-security skill
- backend-architect agent
- api-contract-validation skill

### Validates
- All CRUD operations
- API endpoint handlers
- Database queries
- Route parameter usage

## Success Metrics
- **Query Filtering:** 100% user-scoped queries have user_id filter
- **Route Validation:** 100% route params validated against JWT
- **IDOR Vulnerabilities:** 0
- **Cross-User Access:** 0 possible
- **Isolation Guarantee:** 100% confirmed
