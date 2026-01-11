# Error Normalization & Handling Skill - Specification

## Skill Overview
**Name:** error-normalization-handling
**Type:** Error Management Skill
**Category:** Error Handling & User Experience

## Purpose
Standardizes error handling across frontend and backend to ensure consistent error responses, meaningful user messages, proper HTTP status codes, and aligned error handling patterns.

## Input Requirements
- Backend error handling code
- API error responses
- Frontend error handling logic
- Error message constants
- HTTP status code usage

## Core Functions

### 1. Error Response Normalization
- Define standard error format
- Ensure consistent structure
- Validate error payload
- Review error serialization
- Check error details inclusion

### 2. HTTP Status Code Validation
- Verify correct status code usage
- Check semantic accuracy
- Validate error code ranges
- Review status code consistency
- Ensure RESTful conventions

### 3. Error Message Quality
- Ensure user-friendly messages
- Remove technical jargon
- Validate actionable guidance
- Review message tone
- Check localization support

### 4. Frontend-Backend Alignment
- Validate error format consistency
- Check error code mapping
- Verify status code handling
- Review error transformation
- Ensure contract compliance

### 5. Error Recovery Patterns
- Validate retry mechanisms
- Check fallback strategies
- Review error boundaries
- Verify graceful degradation
- Test recovery flows

## Error Standards

### Standard Error Response Format (Backend)
```python
# ✓ CORRECT - Standard error format
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class APIError(Exception):
    def __init__(self, status_code: int, message: str, error_code: str = None):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code or f"ERR_{status_code}"

@app.exception_handler(APIError)
async def api_error_handler(request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error": exc.error_code,
            "status_code": exc.status_code
        }
    )

# Usage
if not todo:
    raise APIError(404, "Todo not found", "TODO_NOT_FOUND")

# Response:
# Status: 404
# Body: {
#   "detail": "Todo not found",
#   "error": "TODO_NOT_FOUND",
#   "status_code": 404
# }

# ✗ INCORRECT - Inconsistent error format
@app.get("/todos/{id}")
def get_todo(id: int):
    todo = get_todo_by_id(id)
    if not todo:
        return {"error": "Not found"}  # Wrong format, no status code

# ✗ INCORRECT - Technical details exposed
try:
    result = db.execute(query)
except Exception as e:
    raise HTTPException(500, str(e))  # Exposes SQL details
```

### HTTP Status Code Standards
```
1xx Informational (rarely used in APIs)
100 Continue

2xx Success
200 OK - Successful GET, PUT, PATCH
201 Created - Successful POST
204 No Content - Successful DELETE

3xx Redirection
301 Moved Permanently
302 Found (Temporary Redirect)

4xx Client Errors
400 Bad Request - Invalid request format/syntax
401 Unauthorized - Missing or invalid authentication
403 Forbidden - Authenticated but insufficient permissions
404 Not Found - Resource doesn't exist
405 Method Not Allowed - Wrong HTTP method
409 Conflict - Resource conflict (e.g., duplicate)
422 Unprocessable Entity - Validation errors
429 Too Many Requests - Rate limit exceeded

5xx Server Errors
500 Internal Server Error - Unexpected server error
502 Bad Gateway - Upstream service error
503 Service Unavailable - Temporary unavailability
504 Gateway Timeout - Upstream timeout
```

### Error Message Guidelines
```python
# ✓ CORRECT - User-friendly messages
ERROR_MESSAGES = {
    "TODO_NOT_FOUND": "The todo you're looking for doesn't exist.",
    "UNAUTHORIZED": "Please log in to continue.",
    "FORBIDDEN": "You don't have permission to do that.",
    "VALIDATION_ERROR": "Please check your input and try again.",
    "SERVER_ERROR": "Something went wrong on our end. Please try again later.",
}

# ✗ INCORRECT - Technical messages
ERROR_MESSAGES = {
    "TODO_NOT_FOUND": "SELECT query returned NULL",
    "UNAUTHORIZED": "JWT signature verification failed",
    "FORBIDDEN": "User role != admin",
}
```

### Frontend Error Handling
```typescript
// ✓ CORRECT - Consistent error handling
interface APIError {
  detail: string
  error: string
  status_code: number
}

function handleAPIError(error: any): string {
  if (error.response) {
    const apiError: APIError = error.response.data
    const statusCode = error.response.status

    // Map status codes to user-friendly messages
    switch (statusCode) {
      case 400:
        return apiError.detail || 'Invalid request. Please check your input.'
      case 401:
        handleUnauthorized()
        return 'Please log in to continue.'
      case 403:
        return 'You don\'t have permission to perform this action.'
      case 404:
        return apiError.detail || 'The item you\'re looking for doesn\'t exist.'
      case 409:
        return apiError.detail || 'This item already exists.'
      case 422:
        return apiError.detail || 'Please check your input and try again.'
      case 429:
        return 'Too many requests. Please slow down.'
      case 500:
      case 502:
      case 503:
      case 504:
        return 'Server error. Please try again later.'
      default:
        return apiError.detail || 'An unexpected error occurred.'
    }
  } else if (error.request) {
    return 'Network error. Please check your connection.'
  } else {
    return 'An unexpected error occurred.'
  }
}

// ✗ INCORRECT - No error standardization
function handleError(error: any) {
  alert(error.message)  // May show technical details
}
```

## Validation Process

### Step 1: Backend Error Audit
1. Find all error throwing code
2. Check status code usage
3. Validate error format
4. Review error messages
5. Test error responses

### Step 2: Frontend Error Review
1. Locate error handling logic
2. Check error transformation
3. Validate user messages
4. Review error display
5. Test error scenarios

### Step 3: Status Code Validation
1. List all endpoint status codes
2. Verify semantic correctness
3. Check consistency
4. Validate against REST standards
5. Test edge cases

### Step 4: Message Quality Check
1. Review all error messages
2. Check for technical jargon
3. Ensure actionability
4. Validate tone consistency
5. Test user comprehension

### Step 5: Integration Testing
1. Trigger various errors
2. Check frontend handling
3. Verify status codes
4. Test error recovery
5. Validate user experience

## Output Format

### Error Handling Compliance Report
```markdown
## ERROR NORMALIZATION & HANDLING REPORT

**Overall Status:** [COMPLIANT | NEEDS IMPROVEMENT | NON-COMPLIANT]
**Error Endpoints Analyzed:** 24
**Compliant:** 18 (75%)
**Issues Found:** 6 (25%)

### ✓ Compliant Error Handling
1. **POST /todos (Validation Error)**
   - Status Code: ✓ 422 Unprocessable Entity
   - Format: ✓ Standard {detail, error, status_code}
   - Message: ✓ "Title is required"
   - Frontend: ✓ Displays user-friendly message

2. **GET /todos/{id} (Not Found)**
   - Status Code: ✓ 404 Not Found
   - Format: ✓ Standard format
   - Message: ✓ "Todo not found"
   - Frontend: ✓ Shows "Item doesn't exist"

### ⚠ Inconsistent Patterns
3. **DELETE /todos/{id} (Server Error)**
   - Status Code: ✓ 500 Internal Server Error
   - Format: ⚠ Different structure: {error: {message}}
   - Message: ⚠ Technical: "NoneType has no attribute 'id'"
   - Frontend: ✗ Doesn't parse this format
   - **Fix:** Use standard format, hide technical details

### ✗ Non-Compliant
4. **PUT /todos/{id} (Unauthorized)**
   - Status Code: ✗ 400 Bad Request (should be 401)
   - Format: ✗ Plain text "Unauthorized"
   - Message: ✗ No detail
   - Frontend: ✗ Shows "Error occurred"
   - **Fix:** Return 401 with standard JSON format

5. **POST /auth/login (Invalid Credentials)**
   - Status Code: ⚠ 400 Bad Request (401 would be clearer)
   - Format: ✓ Standard format
   - Message: ✗ "Authentication failed"  (too vague)
   - Frontend: ✓ Handles correctly
   - **Fix:** More specific message: "Invalid email or password"
```

### Inconsistent Patterns
```markdown
## INCONSISTENT PATTERNS DETECTED

### Format Inconsistencies
1. **Most endpoints use:**
   ```json
   {
     "detail": "Error message",
     "error": "ERROR_CODE",
     "status_code": 400
   }
   ```

2. **But DELETE /todos/{id} uses:**
   ```json
   {
     "error": {
       "message": "Error message",
       "code": "ERROR_CODE"
     }
   }
   ```
   **Impact:** Frontend can't reliably parse errors
   **Fix:** Standardize all endpoints to format #1

### Status Code Misuse
1. **401 vs 403 Confusion**
   - Several endpoints return 401 for permission errors
   - Should use 403 when authenticated but forbidden
   - **Fix:**
     - 401: Missing or invalid token
     - 403: Valid token but insufficient permissions

2. **400 Overuse**
   - Used for validation (should be 422)
   - Used for not found (should be 404)
   - Used for unauthorized (should be 401)
   - **Fix:** Use specific status codes

### Message Quality Issues
1. **Technical Messages Exposed**
   - "SELECT * FROM todos WHERE id = 123 failed"
   - "NoneType object has no attribute 'user_id'"
   - **Fix:** Map to user-friendly messages

2. **Vague Messages**
   - "Error occurred"
   - "Invalid request"
   - **Fix:** Be specific: "Title must be between 1 and 200 characters"
```

### Standardization Recommendations
```markdown
## STANDARDIZATION RECOMMENDATIONS

### 1. Backend Error Handler
```python
# utils/errors.py
from enum import Enum
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class ErrorCode(str, Enum):
    # Authentication & Authorization
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

    # Resource Errors
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"

    # Validation Errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"

    # Server Errors
    INTERNAL_ERROR = "INTERNAL_ERROR"

class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: ErrorCode = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or ErrorCode.INTERNAL_ERROR

@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error": exc.error_code.value,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the actual error
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Return generic message to user
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "error": ErrorCode.INTERNAL_ERROR.value,
            "status_code": 500
        }
    )

# Usage
@app.get("/todos/{id}")
def get_todo(id: int, user: User = Depends(get_current_user)):
    todo = session.get(Todo, id)
    if not todo:
        raise APIException(404, "Todo not found", ErrorCode.NOT_FOUND)
    if todo.user_id != user.id:
        raise APIException(403, "You don't have permission to access this todo", ErrorCode.FORBIDDEN)
    return todo
```

### 2. Frontend Error Handler
```typescript
// utils/errorHandler.ts
import { ErrorCode } from './errorCodes'

export interface APIError {
  detail: string
  error: string
  status_code: number
}

export class ErrorHandler {
  static handle(error: any): string {
    if (error.response) {
      const apiError: APIError = error.response.data
      return this.getMessageForCode(apiError)
    } else if (error.request) {
      return 'Network error. Please check your internet connection.'
    } else {
      return 'An unexpected error occurred. Please try again.'
    }
  }

  private static getMessageForCode(error: APIError): string {
    // First try to use the detail from API
    if (error.detail && !this.isTechnicalMessage(error.detail)) {
      return error.detail
    }

    // Otherwise map error code to user-friendly message
    const messages: Record<string, string> = {
      [ErrorCode.UNAUTHORIZED]: 'Please log in to continue.',
      [ErrorCode.FORBIDDEN]: 'You don\'t have permission to do that.',
      [ErrorCode.NOT_FOUND]: 'The item you\'re looking for doesn\'t exist.',
      [ErrorCode.ALREADY_EXISTS]: 'This item already exists.',
      [ErrorCode.VALIDATION_ERROR]: 'Please check your input and try again.',
      [ErrorCode.INVALID_CREDENTIALS]: 'Invalid email or password.',
      [ErrorCode.INTERNAL_ERROR]: 'Something went wrong. Please try again later.',
    }

    return messages[error.error] || error.detail || 'An error occurred.'
  }

  private static isTechnicalMessage(message: string): boolean {
    const technicalKeywords = ['exception', 'stack', 'null', 'undefined', 'attribute', 'SELECT']
    return technicalKeywords.some(keyword =>
      message.toLowerCase().includes(keyword.toLowerCase())
    )
  }
}

// Usage
try {
  await api.deleteTodo(id)
  showSuccess('Todo deleted')
} catch (error) {
  const message = ErrorHandler.handle(error)
  showError(message)
}
```

### 3. Validation Error Format
```python
# For 422 validation errors
from pydantic import BaseModel, ValidationError

@app.post("/todos")
def create_todo(todo: TodoCreate):
    # Pydantic automatically validates
    # On validation error, FastAPI returns:
    {
      "detail": [
        {
          "loc": ["body", "title"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }

# Better: Transform to standard format
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = '.'.join(str(loc) for loc in error['loc'][1:])
        errors.append(f"{field}: {error['msg']}")

    return JSONResponse(
        status_code=422,
        content={
            "detail": "; ".join(errors),
            "error": "VALIDATION_ERROR",
            "status_code": 422,
            "fields": {
                error['loc'][-1]: error['msg']
                for error in exc.errors()
            }
        }
    )
```
```

## Common Error Handling Anti-Patterns

### Anti-Pattern 1: Generic Errors
```python
# ❌ BAD
raise HTTPException(400, "Error")

# ✓ GOOD
raise APIException(400, "Title must be between 1 and 200 characters", ErrorCode.VALIDATION_ERROR)
```

### Anti-Pattern 2: Exposing Technical Details
```python
# ❌ BAD
except Exception as e:
    raise HTTPException(500, str(e))  # May expose SQL, stack traces

# ✓ GOOD
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise APIException(500, "An unexpected error occurred", ErrorCode.INTERNAL_ERROR)
```

### Anti-Pattern 3: Wrong Status Codes
```python
# ❌ BAD
if not todo:
    raise HTTPException(400, "Not found")  # Should be 404

# ✓ GOOD
if not todo:
    raise APIException(404, "Todo not found", ErrorCode.NOT_FOUND)
```

### Anti-Pattern 4: Inconsistent Frontend Handling
```typescript
// ❌ BAD
catch (error) {
  alert(error.message)  // Different handling everywhere
}

// ✓ GOOD
catch (error) {
  const message = ErrorHandler.handle(error)  // Centralized
  showError(message)
}
```

## Integration Points

### Works With
- backend-architect agent
- frontend-api-integration skill
- api-contract-validation skill
- ui-state-management skill

### Validates
- Error response formats
- HTTP status code usage
- Error message quality
- Frontend-backend alignment

### Provides
- Error standardization guidelines
- Status code mapping
- User-friendly message templates
- Error handling patterns

## Success Metrics
- **Error Format:** 100% use standard format
- **Status Codes:** 100% semantically correct
- **User Messages:** 100% non-technical
- **Frontend Alignment:** 100% errors handled
- **Technical Details Exposed:** 0
