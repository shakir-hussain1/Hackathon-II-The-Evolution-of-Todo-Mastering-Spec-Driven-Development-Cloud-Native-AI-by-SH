# Prompt History Record: frontend-api-integration Skill

## Creation Date
2026-01-11

## Skill Type
Integration Validation Skill

## Purpose
Validates frontend-backend interaction by checking API base URL, JWT attachment, error handling, and CORS configuration.

## Key Functions
1. API base URL validation (env variables)
2. JWT attachment verification (interceptors)
3. Error handling validation (try-catch, user feedback)
4. CORS configuration review
5. Network misconfiguration detection

## Critical Checks
- Base URL from environment (not hardcoded)
- JWT in Authorization header (Bearer token)
- Comprehensive error handling
- HTTPS in production
- Proper CORS configuration
- Timeout handling
- Retry logic

## Common Issues
- Hardcoded API URLs
- Missing JWT in requests
- Silent error failures
- CORS misconfiguration
- Mixed content (http/https)
- No request timeouts
- Token in URL parameters

## Usage Patterns
- After API client setup
- When auth integration changes
- For network error debugging
- Before production deployment
- Integration testing

## Integration Points
- Works with frontend-ui-dashboard
- Validates auth-security-validator
- Supports api-contract-validation
- Feeds error-normalization-handling

## Success Metrics
- **Base URL Config:** 100% use env variables
- **JWT Attachment:** 100% protected endpoints
- **Error Handling:** 100% requests wrapped
- **CORS Errors:** 0 in production
- **Network Failures:** 100% handled
