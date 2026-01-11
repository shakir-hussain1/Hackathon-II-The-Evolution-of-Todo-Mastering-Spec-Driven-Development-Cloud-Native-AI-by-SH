# Prompt History Record: auth-security-validator Agent

## Creation Date
2026-01-11

## Agent Type
Security Specialist

## Purpose
Created to validate authentication flows, JWT implementation, and all security-critical code to prevent vulnerabilities in user authentication and authorization systems.

## Creation Context
Developed for the Hackathon II project to ensure robust security practices and prevent common authentication vulnerabilities like auth bypass, IDOR, and token manipulation.

## Key Capabilities
1. Authentication flow validation (registration, login, password reset)
2. JWT token security review (generation, verification, storage)
3. Protected route security assessment
4. Vulnerability detection (IDOR, privilege escalation, auth bypass)
5. Cross-user access prevention
6. Security best practices enforcement

## Usage Patterns

### Primary Use Cases
- After implementing auth endpoints
- When adding protected routes
- Before merging auth-related code
- During PR review of authentication
- After user-facing auth features
- For security audits

### Trigger Conditions
- New authentication endpoints
- Modified JWT logic
- Protected route changes
- User permission updates
- Security vulnerability reports
- Pre-production security checks

## Integration with Project
- Works with jwt-verification-security skill
- Validates backend-architect implementations
- Coordinates with user-ownership-enforcement skill
- Feeds security findings to quality-readiness-validation
- Supports api-contract-validation

## Security Focus Areas

### Authentication
- Password hashing (bcrypt cost≥12 or argon2)
- Secure password requirements
- Rate limiting (5 attempts/15 min)
- Email uniqueness enforcement
- Token generation security
- Session management

### JWT Implementation
- Strong secret (≥256 bits)
- Proper signature verification
- Expiry validation (15-60 min access)
- Refresh token rotation
- Secure storage (httpOnly cookies)
- No sensitive data in payload

### Authorization
- Middleware on protected routes
- JWT verification before handlers
- User identity extraction
- Authorization checks
- Data ownership validation
- Audit logging

### Vulnerability Prevention
- Auth bypass protection
- IDOR prevention
- Privilege escalation blocking
- Token manipulation detection
- Session fixation prevention
- Credential leakage avoidance

## Evolution Notes
- Started with basic auth validation
- Added comprehensive JWT checks
- Enhanced IDOR detection
- Integrated OWASP Top 10 checks
- Improved vulnerability reporting

## Best Practices
- Run before auth code merges
- Validate all protected endpoints
- Check user data isolation
- Review token handling
- Test security scenarios

## Common Vulnerabilities Detected

### Critical
- Missing authentication middleware
- Weak password requirements
- No rate limiting
- Auth bypass vulnerabilities
- IDOR in data access

### High
- Weak JWT secrets
- No token expiry
- Tokens in localStorage
- Missing ownership checks
- Privilege escalation risks

### Medium
- Long token expiry
- Poor error messages
- Missing audit logs
- Inconsistent auth patterns

## Vulnerability Report Format
```
Vulnerability: [Name]
Severity: [Critical/High/Medium/Low]
Location: [File:Line]
Description: [Issue details]
Impact: [What could happen]
Proof of Concept: [How to exploit]
Remediation: [How to fix]
References: [OWASP, CWE]
```

## Security Standards Enforced
- OWASP Top 10
- CWE/SANS Top 25
- NIST guidelines
- JWT RFC 7519
- OAuth 2.0 best practices

## Success Metrics
- Zero critical auth vulnerabilities
- 100% protected routes authenticated
- All user data properly isolated
- No auth bypass possible
- Comprehensive audit logging

## Maintenance
- Update vulnerability database
- Refine detection patterns
- Keep OWASP standards current
- Review new attack vectors
- Update remediation guidance
