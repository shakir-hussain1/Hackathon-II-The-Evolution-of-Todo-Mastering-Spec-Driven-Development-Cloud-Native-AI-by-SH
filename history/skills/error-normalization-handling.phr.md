# Prompt History Record: error-normalization-handling Skill

## Creation Date
2026-01-11

## Skill Type
Error Management Skill

## Purpose
Standardizes error handling across frontend and backend ensuring consistent error responses, meaningful messages, and proper HTTP status codes.

## Key Functions
1. Error response format normalization
2. HTTP status code validation
3. Error message quality review
4. Frontend-backend alignment validation
5. Error recovery pattern implementation

## Standard Error Format
```json
{
  "detail": "User-friendly message",
  "error": "ERROR_CODE",
  "status_code": 400
}
```

## Status Code Standards
- 200/201/204: Success
- 400: Bad request
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 422: Validation error
- 429: Rate limited
- 500: Server error

## Common Issues
- Inconsistent error formats
- Wrong status codes (e.g., 400 for everything)
- Technical error messages exposed
- No frontend error handling
- Silent failures

## Message Guidelines
- User-friendly (no technical jargon)
- Actionable (tell user what to do)
- Consistent tone
- Never expose stack traces
- Map technical to user messages

## Usage Patterns
- After error handling implementation
- During API standardization
- For error UX improvement
- Before production deployment
- Code review validation

## Integration Points
- Works with backend-architect
- Validates frontend-api-integration
- Supports api-contract-validation
- Feeds ui-state-management

## Success Metrics
- **Error Format:** 100% standard format
- **Status Codes:** 100% semantically correct
- **User Messages:** 100% non-technical
- **Frontend Alignment:** 100% handled
- **Technical Details Exposed:** 0
