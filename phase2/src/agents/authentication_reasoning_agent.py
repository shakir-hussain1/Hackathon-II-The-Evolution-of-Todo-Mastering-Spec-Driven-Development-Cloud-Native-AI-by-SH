"""
Authentication Reasoning Agent
Purpose: Reason about Better Auth + JWT integration across frontend and backend
Responsibility: JWT flow, verification logic, shared-secret requirements, bypass risks
"""

class AuthenticationReasoningAgent:
    """Reasons about authentication flow and JWT validation"""

    def __init__(self):
        self.jwt_rules = {}
        self.auth_flow = []
        self.security_risks = []

    def define_jwt_issuance_flow(self) -> dict:
        """Define how JWT tokens are issued"""
        return {
            "issuer": "Better Auth",
            "claims": ["user_id", "exp", "iat"],
            "algorithm": "HS256",
            "flow": [
                "1. User signs up/logs in with Better Auth",
                "2. Better Auth validates credentials",
                "3. JWT token issued containing user_id",
                "4. Token returned to frontend",
                "5. Frontend stores token in secure storage",
            ],
        }

    def define_jwt_verification_logic(self) -> dict:
        """Define backend JWT verification"""
        return {
            "location": "Authorization header",
            "format": "Bearer <token>",
            "verification_steps": [
                "1. Extract token from Authorization header",
                "2. Verify JWT signature using shared_secret",
                "3. Check token not expired (exp claim)",
                "4. Extract user_id from token",
                "5. Validate user_id matches URL parameter",
                "6. Allow/deny request based on match",
            ],
        }

    def define_shared_secret_requirements(self) -> dict:
        """Define shared secret for JWT signing"""
        return {
            "name": "JWT_SECRET",
            "location": "Environment variable (both frontend, backend)",
            "usage": "Sign and verify JWT tokens",
            "rotation": "Should be rotated on compromise",
            "security": "Never hardcode, use env vars only",
        }

    def detect_auth_bypass_risks(self) -> list:
        """Identify potential auth bypass vectors"""
        risks = [
            "Expired token still accepted",
            "Missing JWT verification on endpoint",
            "user_id not validated against token",
            "JWT secret hardcoded",
            "Token stored in localStorage (XSS vulnerability)",
            "CORS misconfiguration allowing token theft",
        ]
        return risks

    def generate_auth_flow_reasoning(self) -> dict:
        """Complete auth flow documentation"""
        return {
            "issuance": self.define_jwt_issuance_flow(),
            "verification": self.define_jwt_verification_logic(),
            "secret": self.define_shared_secret_requirements(),
            "risks": self.detect_auth_bypass_risks(),
        }
