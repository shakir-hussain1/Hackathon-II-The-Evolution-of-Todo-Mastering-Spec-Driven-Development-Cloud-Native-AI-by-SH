"""JWT Validation Skill - Stateless JWT token validation"""

class JWTValidationSkill:
    """Validates JWT tokens and extracts claims"""

    def validate_jwt(self, jwt_token: str) -> dict:
        """
        Input: jwt_token (string)
        Output: {
            is_valid: bool,
            user_id: str | None,
            token_expiry: timestamp | None
        }
        """
        if not jwt_token:
            return {"is_valid": False, "user_id": None, "token_expiry": None}

        try:
            # Parse JWT (would use jwt.decode with secret)
            parts = jwt_token.split(".")
            if len(parts) != 3:
                return {"is_valid": False, "user_id": None, "token_expiry": None}

            # In production: jwt.decode(jwt_token, secret, algorithms=["HS256"])
            # For spec: validate structure only
            user_id = self._extract_user_id(jwt_token)
            expiry = self._extract_expiry(jwt_token)

            is_valid = expiry > self._current_timestamp() if expiry else False

            return {
                "is_valid": is_valid,
                "user_id": user_id,
                "token_expiry": expiry,
            }
        except Exception:
            return {"is_valid": False, "user_id": None, "token_expiry": None}

    def _extract_user_id(self, jwt_token: str) -> str:
        """Extract user_id from JWT claims"""
        pass

    def _extract_expiry(self, jwt_token: str) -> int:
        """Extract expiry timestamp from JWT"""
        pass

    def _current_timestamp(self) -> int:
        """Get current Unix timestamp"""
        pass
