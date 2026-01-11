# Prompt History Record: user-ownership-enforcement Skill

## Creation Date
2026-01-11

## Skill Type
Security Validation Skill

## Purpose
Ensures strict data ownership and isolation by validating all queries are filtered by authenticated user ID, preventing cross-user data access.

## Key Functions
1. Query filtering validation (user_id presence)
2. Route parameter vs JWT validation
3. CRUD operation ownership checks
4. IDOR vulnerability detection
5. Data isolation verification

## Critical Rules
- ALL user-scoped queries MUST filter by user_id
- Route parameters MUST be validated against JWT
- Updates/Deletes MUST verify ownership
- List endpoints MUST filter by current user
- Zero cross-user access allowed

## Common Vulnerabilities
- Missing user_id filters on queries
- Trusting route parameters (IDOR)
- No ownership check before modification
- Admin bypass opportunities
- Privilege escalation risks

## Usage Patterns
- After implementing CRUD operations
- When adding new endpoints
- During security audits
- Before production deployment
- Code review validation

## Integration Points
- Works with auth-security-validator
- Validates backend-architect code
- Supports jwt-verification-security
- Feeds api-contract-validation

## Success Metrics
- **Query Filtering:** 100% user-scoped queries filtered
- **Route Validation:** 100% params validated against JWT
- **IDOR Vulnerabilities:** 0
- **Cross-User Access:** 0 possible
- **Isolation Guarantee:** 100% confirmed
