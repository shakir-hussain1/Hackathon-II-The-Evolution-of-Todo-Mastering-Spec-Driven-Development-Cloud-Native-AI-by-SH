# API Contract Validation Skill - Specification

## Skill Overview
**Name:** api-contract-validation
**Type:** API Quality Assurance Skill
**Category:** Contract Testing & Validation

## Purpose
Validates that API implementation matches defined specifications by checking endpoints, HTTP methods, status codes, request/response schemas, and detecting undocumented endpoints.

## Input Requirements
- API specification documents (OpenAPI, manual specs)
- Backend route definitions
- API handler implementations
- Request/response model definitions
- Example requests/responses

## Core Functions

### 1. Endpoint Verification
- Match implemented routes to spec
- Verify URL path patterns
- Check path parameters
- Validate query parameters
- Confirm endpoint existence

### 2. HTTP Method Validation
- Verify correct methods (GET/POST/PUT/DELETE/PATCH)
- Check method semantics (idempotency, safety)
- Validate method-specific behavior
- Ensure RESTful conventions

### 3. Status Code Validation
- Confirm success status codes (200, 201, 204)
- Verify error status codes (400, 401, 403, 404, 500)
- Check status code semantics
- Validate error response format

### 4. Request Schema Validation
- Verify request body structure
- Check required vs. optional fields
- Validate field types and formats
- Confirm validation rules

### 5. Response Schema Validation
- Verify response body structure
- Check field presence and types
- Validate nested objects/arrays
- Confirm pagination format

### 6. Undocumented Endpoint Detection
- Scan implementation for all routes
- Cross-reference with spec
- Flag unspecified endpoints
- Identify spec drift

## Validation Rules

### RESTful Conventions
```
Resource: /todos

GET    /todos       - List all (200)
POST   /todos       - Create (201)
GET    /todos/{id}  - Get one (200 or 404)
PUT    /todos/{id}  - Update (200 or 404)
DELETE /todos/{id}  - Delete (204 or 404)
```

### Status Code Standards
```
2xx Success:
- 200 OK - Successful GET, PUT, PATCH
- 201 Created - Successful POST
- 204 No Content - Successful DELETE

4xx Client Error:
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid auth
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource doesn't exist
- 422 Unprocessable Entity - Validation error

5xx Server Error:
- 500 Internal Server Error - Unexpected error
```

### Response Format Standards
```json
// Success Response
{
  "id": 123,
  "title": "Buy milk",
  "completed": false,
  "user_id": 456
}

// Error Response (standard format)
{
  "detail": "Error message",
  "error": "ERROR_CODE",
  "status_code": 400
}

// List Response (with pagination)
{
  "items": [...],
  "total": 100,
  "page": 1,
  "per_page": 20
}
```

## Validation Process

### Step 1: Spec Parsing
1. Parse API specification
2. Extract all defined endpoints
3. Document expected behavior
4. Build contract database

### Step 2: Implementation Discovery
1. Scan backend code for routes
2. Extract route definitions
3. Identify handler functions
4. Map request/response models

### Step 3: Contract Comparison
1. For each spec endpoint, find implementation
2. For each implementation, find spec
3. Compare methods, parameters, schemas
4. Identify mismatches

### Step 4: Compliance Testing
1. Test each endpoint with valid requests
2. Test error conditions
3. Verify response schemas
4. Check status codes

### Step 5: Gap Analysis
1. List spec items not implemented
2. List implemented routes not in spec
3. Identify schema mismatches
4. Generate fix recommendations

## Output Format

### API Compliance Checklist
```markdown
## API CONTRACT VALIDATION

**Overall Status:** [COMPLIANT | PARTIAL | NON-COMPLIANT]
**Endpoints in Spec:** 12
**Endpoints Implemented:** 14
**Fully Compliant:** 9
**Deviations Found:** 3
**Undocumented:** 2

### ✓ Compliant Endpoints
1. **GET /todos**
   - Status: ✓ Compliant
   - Method: ✓ Correct (GET)
   - Status Codes: ✓ 200, 401
   - Response Schema: ✓ Matches spec

2. **POST /todos**
   - Status: ✓ Compliant
   - Method: ✓ Correct (POST)
   - Status Codes: ✓ 201, 400, 401
   - Request Schema: ✓ Matches spec
   - Response Schema: ✓ Matches spec

### ⚠ Partial Compliance
3. **GET /todos/{id}**
   - Status: ⚠ Partial
   - Method: ✓ Correct (GET)
   - Status Codes: ✗ Returns 500 instead of 404 on not found
   - Response Schema: ✓ Matches spec
   - **Fix:** Return 404 with proper error message

### ✗ Non-Compliant
4. **PUT /todos/{id}**
   - Status: ✗ Non-Compliant
   - Method: ✓ Correct (PUT)
   - Status Codes: ✓ 200, 404, 401
   - Request Schema: ✗ Missing 'priority' field from spec
   - Response Schema: ✗ Extra 'created_at' field not in spec
   - **Fix:** Add priority field, remove created_at or update spec

### 🚨 Undocumented Endpoints
5. **POST /todos/bulk**
   - Status: ❌ Not in spec
   - Implementation: api/todos.py:145
   - **Action:** Add to spec or remove from code

6. **GET /todos/search**
   - Status: ❌ Not in spec
   - Implementation: api/todos.py:167
   - **Action:** Document in API spec
```

### Deviations from Spec
```markdown
## DEVIATIONS DETECTED

### Schema Mismatches
1. **Endpoint:** POST /todos
   - **Field:** `due_date`
   - **Spec:** Required field, format: ISO8601
   - **Implementation:** Optional field, format: "YYYY-MM-DD"
   - **Impact:** Client contracts may break
   - **Fix:** Make required, accept ISO8601 format

2. **Endpoint:** GET /todos/{id}
   - **Field:** `tags`
   - **Spec:** Array of strings
   - **Implementation:** Comma-separated string
   - **Impact:** Type mismatch
   - **Fix:** Return array of strings

### Status Code Mismatches
1. **Endpoint:** DELETE /todos/{id}
   - **Spec:** Return 204 No Content on success
   - **Implementation:** Returns 200 OK with body
   - **Impact:** RESTful convention violation
   - **Fix:** Return 204 with no body

2. **Endpoint:** POST /todos
   - **Spec:** Return 400 on validation error
   - **Implementation:** Returns 422 Unprocessable Entity
   - **Impact:** Minor - 422 is acceptable for validation
   - **Fix:** Update spec to accept 422, or change code to 400

### Missing Endpoints
1. **GET /todos/stats**
   - **In Spec:** Yes
   - **Implemented:** No
   - **Impact:** Feature gap
   - **Fix:** Implement endpoint or remove from spec
```

### Required Fixes
```markdown
## REQUIRED FIXES (Prioritized)

### CRITICAL (Must fix before release)
1. Implement missing endpoint: GET /todos/stats
2. Fix schema mismatch: POST /todos due_date field
3. Document undocumented endpoints or remove them

### HIGH (Should fix soon)
1. Fix status code: DELETE /todos/{id} return 204
2. Fix schema: GET /todos/{id} tags field type
3. Add missing error responses to specs

### MEDIUM (Improve for consistency)
1. Standardize error response format across all endpoints
2. Add pagination to all list endpoints
3. Document rate limiting headers

### LOW (Nice to have)
1. Add OpenAPI/Swagger documentation
2. Include example requests/responses
3. Document optional query parameters
```

## Contract Testing Examples

### Request Schema Validation
```python
# SPEC DEFINITION
class TodoCreate(BaseModel):
    title: str  # Required, max 200 chars
    description: str | None  # Optional
    priority: int  # Required, 1-5
    due_date: datetime  # Required, ISO8601

# ✓ COMPLIANT IMPLEMENTATION
@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate, user: User = Depends(get_current_user)):
    # Schema automatically validated by Pydantic
    db_todo = Todo(**todo.dict(), user_id=user.id)
    session.add(db_todo)
    session.commit()
    return db_todo

# ✗ NON-COMPLIANT (missing validation)
@app.post("/todos", status_code=201)
def create_todo(data: dict):  # No schema validation
    db_todo = Todo(**data)  # Missing required fields not caught
    session.add(db_todo)
    session.commit()
    return db_todo
```

### Response Schema Validation
```python
# SPEC DEFINITION
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

# ✓ COMPLIANT
@app.get("/todos/{id}", response_model=TodoResponse)
def get_todo(id: int):
    return session.get(Todo, id)  # Pydantic ensures schema match

# ✗ NON-COMPLIANT (extra fields)
@app.get("/todos/{id}")
def get_todo(id: int):
    todo = session.get(Todo, id)
    return {
        **todo.dict(),
        "created_at": todo.created_at,  # Not in spec
        "internal_id": todo.uuid  # Internal field leaked
    }
```

## Integration Points

### Works With
- backend-architect agent
- api-contract-validation skill
- error-normalization-handling skill
- frontend-api-integration skill

### Validates Against
- OpenAPI/Swagger specs
- Manual API documentation
- API design documents
- Contract tests

### Provides To
- Frontend teams for contract compliance
- QA for test case generation
- Documentation teams for accuracy
- Backend teams for implementation gaps

## Success Metrics
- **Endpoint Coverage:** 100% spec endpoints implemented
- **Schema Compliance:** 100% match spec definitions
- **Status Code Accuracy:** 100% use correct codes
- **Undocumented Endpoints:** 0
- **Contract Tests Passing:** 100%
