# Prompt History Record: jwt-verification-security Skill

## Creation Date
2026-01-11

## Skill Type
Security Validation Skill

## Purpose
Validates JWT-based authentication implementation to ensure tokens are generated, verified, and handled securely according to industry best practices.

## Key Functions
1. Token presence and format validation
2. Signature verification security
3. Expiry and claims validation
4. User identity extraction review
5. Security risk detection

## Security Standards
- Secret key: ≥256 bits entropy
- Access token expiry: 15-60 minutes
- Refresh token: 7-30 days
- Algorithm: HS256/RS256 (no "none")
- Storage: httpOnly secure cookies preferred

## Common Vulnerabilities Detected
- Weak JWT secrets
- Missing expiry validation
- Algorithm confusion attacks
- Token in localStorage (XSS risk)
- Sensitive data in payload

## Usage Patterns
- After auth endpoint implementation
- During JWT logic changes
- Before production deployment
- For security audits
- Code review validation

## Integration Points
- Works with auth-security-validator agent
- Validates backend-architect code
- Supports user-ownership-enforcement
- Feeds quality-readiness-validation

## Success Metrics
- **Secret Strength:** 100% keys ≥256 bits
- **Expiry Validation:** 100% tokens checked
- **Algorithm Security:** 0 "none" usage
- **Storage Security:** 100% secure storage
- **Critical Vulnerabilities:** 0
