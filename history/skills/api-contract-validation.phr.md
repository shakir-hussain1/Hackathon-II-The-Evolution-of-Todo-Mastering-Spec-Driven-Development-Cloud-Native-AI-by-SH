# Prompt History Record: api-contract-validation Skill

## Creation Date
2026-01-11

## Skill Type
API Quality Assurance Skill

## Purpose
Validates API implementation matches specifications by checking endpoints, methods, status codes, schemas, and detecting undocumented endpoints.

## Key Functions
1. Endpoint verification against spec
2. HTTP method validation
3. Status code correctness
4. Request/response schema validation
5. Undocumented endpoint detection

## RESTful Standards
- GET /resource - List (200)
- POST /resource - Create (201)
- GET /resource/{id} - Get one (200/404)
- PUT /resource/{id} - Update (200/404)
- DELETE /resource/{id} - Delete (204/404)

## Status Code Standards
- 2xx: Success (200, 201, 204)
- 4xx: Client errors (400, 401, 403, 404, 422)
- 5xx: Server errors (500, 502, 503)

## Usage Patterns
- After API implementation
- During contract testing
- Before frontend integration
- For API documentation validation
- Code review checks

## Integration Points
- Works with backend-architect
- Validates error-normalization-handling
- Supports frontend-api-integration
- Feeds quality-readiness-validation

## Success Metrics
- **Endpoint Coverage:** 100% spec endpoints implemented
- **Schema Compliance:** 100% match spec
- **Status Code Accuracy:** 100% correct
- **Undocumented Endpoints:** 0
- **Contract Tests:** 100% passing
