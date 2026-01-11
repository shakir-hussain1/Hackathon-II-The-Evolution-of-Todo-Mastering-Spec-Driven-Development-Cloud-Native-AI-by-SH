# JWT Verification & Security Skill - Specification

## Skill Overview
**Name:** jwt-verification-security
**Type:** Security Validation Skill
**Category:** Authentication & Security

## Purpose
Validates JWT-based authentication implementation to ensure tokens are generated, verified, and handled securely according to industry best practices.

## Input Requirements
- JWT token generation code
- Token verification middleware
- Authentication endpoints
- Secret key configuration
- Token payload structure

## Core Functions

### 1. Token Presence Validation
- Verify token is required on protected routes
- Check Authorization header format
- Validate Bearer scheme usage
- Ensure token is extracted correctly

### 2. Token Format Validation
- Verify JWT structure (header.payload.signature)
- Check header algorithm (HS256/RS256)
- Validate payload schema
- Ensure proper Base64URL encoding

### 3. Signature Verification
- Confirm secret key strength (min 256 bits)
- Verify signature algorithm consistency
- Check signature verification process
- Validate key rotation capability

### 4. Expiry & Claims Validation
- Verify 'exp' claim presence
- Check expiration time enforcement
- Validate 'iat' (issued at) claim
- Review custom claims security

### 5. User Identity Extraction
- Verify secure user_id extraction
- Check for injection vulnerabilities
- Validate identity consistency
- Ensure no privilege escalation

### 6. Security Risk Detection
- Identify auth bypass opportunities
- Detect weak secrets
- Find token leakage risks
- Check for algorithm confusion attacks

## Validation Rules

### Token Generation Requirements
```python
# REQUIRED in JWT payload:
{
    "user_id": "<uuid>",      # User identifier
    "exp": <timestamp>,        # Expiration (15-60 min for access token)
    "iat": <timestamp>,        # Issued at
    "type": "access|refresh"   # Token type
}

# FORBIDDEN in JWT payload:
- Passwords or password hashes
- Sensitive personal information
- API keys or secrets
- Full user objects
```

### Secret Key Requirements
- Minimum 256 bits (32 bytes) entropy
- Stored in environment variables
- Never committed to version control
- Rotatable without service disruption
- Different secrets for dev/staging/prod

### Token Expiry Standards
- **Access Token:** 15-60 minutes
- **Refresh Token:** 7-30 days
- Must validate expiry on every request
- Clock skew tolerance: ≤30 seconds

### Signature Algorithm Standards
- **Symmetric:** HS256 with strong secret
- **Asymmetric:** RS256 with 2048+ bit keys
- **Forbidden:** "none" algorithm
- Must not allow algorithm switching

## Validation Process

### Step 1: Configuration Audit
1. Check secret key strength
2. Verify environment variable usage
3. Validate algorithm selection
4. Review expiry settings

### Step 2: Generation Review
1. Analyze token creation code
2. Verify payload contents
3. Check signature process
4. Validate expiry setting

### Step 3: Verification Review
1. Examine middleware implementation
2. Verify signature checking
3. Check expiry validation
4. Review error handling

### Step 4: Security Testing
1. Test with expired tokens
2. Try algorithm confusion
3. Attempt token tampering
4. Test with missing claims

## Output Format

### JWT Validation Checklist
```markdown
## JWT SECURITY VALIDATION

**Overall Status:** [SECURE | VULNERABLE | CRITICAL]

### Token Generation
- [✓] Strong secret key (≥256 bits)
- [✓] Secret in environment variable
- [✓] Appropriate algorithm (HS256/RS256)
- [✓] Expiry claim present
- [✗] Sensitive data in payload (VIOLATION)
- [✓] User ID properly included

### Token Verification
- [✓] Signature verified on every request
- [✓] Expiry checked
- [✓] Algorithm validated
- [✗] No algorithm confusion protection (RISK)
- [✓] User identity extracted securely

### Security Configuration
- [✓] HTTPS enforced in production
- [✓] httpOnly cookies (if used)
- [✓] Secure flag on cookies
- [✗] Token in localStorage (VULNERABILITY)
- [✓] CORS properly configured
```

### Security Risk Assessment
```markdown
## SECURITY RISKS IDENTIFIED

### CRITICAL
1. **Token Storage Vulnerability**
   - **Issue:** JWT stored in localStorage
   - **Impact:** Vulnerable to XSS attacks
   - **Remediation:** Use httpOnly secure cookies
   - **Reference:** OWASP A7:2017 - XSS

### HIGH
2. **Weak Secret Key**
   - **Issue:** Secret is only 128 bits
   - **Impact:** Brute-force possible
   - **Remediation:** Generate 256+ bit secret
   - **Reference:** RFC 7518 Section 3.2

### MEDIUM
3. **Long Token Expiry**
   - **Issue:** Access token valid for 24 hours
   - **Impact:** Extended compromise window
   - **Remediation:** Reduce to 15-60 minutes
   - **Reference:** OAuth 2.0 Best Practices
```

### Pass/Fail Verdict
```markdown
## VERDICT: [PASS | CONDITIONAL PASS | FAIL]

**Status:** FAIL

**Blocking Issues:**
- Critical: Token stored in localStorage
- High: Weak secret key

**Required Fixes:**
1. Implement httpOnly secure cookies for token storage
2. Generate new 256-bit secret key
3. Reduce access token expiry to 15 minutes
4. Implement refresh token rotation

**Conditional Pass Criteria:**
- All CRITICAL issues resolved
- All HIGH issues resolved or accepted risk documented

**Timeline:** Must fix before production deployment
```

## Common Vulnerabilities

### 1. Algorithm Confusion Attack
```python
# VULNERABLE CODE
token = jwt.decode(token_string, verify=False)  # ❌ No verification

# SECURE CODE
token = jwt.decode(
    token_string,
    secret_key,
    algorithms=["HS256"]  # ✓ Algorithm whitelist
)
```

### 2. Secret Key Exposure
```python
# VULNERABLE CODE
SECRET_KEY = "my-secret-key"  # ❌ Hardcoded

# SECURE CODE
import os
SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # ✓ From environment
if len(SECRET_KEY) < 32:
    raise ValueError("JWT secret must be ≥256 bits")
```

### 3. Sensitive Data in Token
```python
# VULNERABLE CODE
payload = {
    "user_id": user.id,
    "password": user.password,  # ❌ NEVER include passwords
    "email": user.email,        # ⚠️ PII in token
}

# SECURE CODE
payload = {
    "user_id": user.id,         # ✓ Minimal identifier only
    "exp": datetime.utcnow() + timedelta(minutes=15),
    "iat": datetime.utcnow()
}
```

### 4. Missing Expiry Validation
```python
# VULNERABLE CODE
try:
    payload = jwt.decode(token, secret)  # ❌ Expiry not checked
except jwt.DecodeError:
    return None

# SECURE CODE
try:
    payload = jwt.decode(
        token,
        secret,
        algorithms=["HS256"],
        options={"verify_exp": True}  # ✓ Enforce expiry
    )
except jwt.ExpiredSignatureError:
    return None  # ✓ Reject expired tokens
```

## Integration Points

### Works With
- auth-security-validator agent
- user-ownership-enforcement skill
- backend-architect agent
- api-contract-validation skill

### Provides To
- Token security assessment
- Configuration recommendations
- Vulnerability findings
- Best practice guidance

## Success Metrics
- **Secret Strength:** 100% keys ≥256 bits
- **Token Expiry:** 100% have exp claim validated
- **Algorithm Security:** 0 "none" algorithm usage
- **Storage Security:** 100% use httpOnly cookies (web) or secure storage (mobile)
- **Critical Vulnerabilities:** 0 in production
