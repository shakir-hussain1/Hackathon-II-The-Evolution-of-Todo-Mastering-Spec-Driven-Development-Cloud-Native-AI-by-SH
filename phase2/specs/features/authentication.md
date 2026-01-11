# Feature: Authentication & JWT Security

**Feature ID**: AUTH-001
**Status**: Specification
**Related Spec**: @specs/overview.md

---

## Overview

Authentication enables multi-user support with secure, stateless JWT tokens issued by Better Auth. Every API request requires a valid JWT token containing the authenticated user's identity.

---

## Requirements

### REQ-AUTH-001: User Registration
- Better Auth handles signup UI and credential storage
- User provides email and password
- Account created in Better Auth database
- User automatically authenticated after signup

### REQ-AUTH-002: User Login
- Better Auth handles login UI and credential validation
- User provides email and password
- Credentials validated securely
- JWT token issued on successful login

### REQ-AUTH-003: JWT Token Issuance
- Better Auth issues JWT with claims:
  - `sub`: user ID (string/UUID)
  - `exp`: expiration (Unix timestamp, 24 hours)
  - `iat`: issued at (Unix timestamp)
- Token signed with `JWT_SECRET` environment variable
- Algorithm: HS256

### REQ-AUTH-004: Token Storage (Frontend)
- JWT token stored in secure location:
  - HttpOnly cookie (secure), OR
  - localStorage (if HttpOnly unavailable)
- Token persists across page reloads
- Token cleared on logout

### REQ-AUTH-005: Token Transmission
- Frontend attaches JWT to every API request
- Location: `Authorization` header
- Format: `Bearer <token>`
- Example: `Authorization: Bearer eyJhbGc...`

### REQ-AUTH-006: Token Validation (Backend)
- Middleware extracts token from Authorization header
- JWT signature verified using `JWT_SECRET`
- Token expiration checked (exp > current time)
- Invalid/expired tokens rejected with 401 Unauthorized

### REQ-AUTH-007: User Identity Extraction
- Middleware decodes JWT claims
- Extracts `sub` (user_id) from token
- Attaches user_id to request context
- Available to route handlers as `request.user_id`

### REQ-AUTH-008: Logout
- Frontend removes JWT from storage
- No backend revocation needed
- Subsequent requests without token → 401

---

## API Contract

### POST /auth/signup (Better Auth)
```
Request:
  body: { email: string, password: string }

Response (201 Created):
  body: { user: { id, email }, token: string }
```

### POST /auth/login (Better Auth)
```
Request:
  body: { email: string, password: string }

Response (200 OK):
  body: { user: { id, email }, token: string }
```

### POST /auth/logout
```
Request:
  Authorization: Bearer <token>

Response (200 OK):
  body: { message: "Logged out successfully" }
```

---

## JWT Token Example

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-123",
    "exp": 1704931200,
    "iat": 1704844800
  }
}
```

---

## Security Rules

1. **No Hardcoded Secrets**: JWT_SECRET in environment variables only
2. **Signature Verification**: Every token verified before use
3. **Expiration Check**: Expired tokens rejected
4. **Token in URL Forbidden**: Token never in query parameters
5. **HTTPS Only** (Production): Tokens transmitted over HTTPS only
6. **HttpOnly Cookies** (Recommended): Prevent XSS token theft

---

## Implementation Checklist

- [ ] Better Auth configured for JWT issuance
- [ ] JWT_SECRET set in .env
- [ ] Frontend stores JWT securely
- [ ] Frontend attaches JWT to API requests
- [ ] Backend middleware validates JWT signature
- [ ] Backend checks token expiration
- [ ] Backend extracts user_id from token
- [ ] All endpoints enforce JWT requirement
- [ ] Invalid tokens return 401
- [ ] Logout clears token

---

**Status**: Ready for Implementation
