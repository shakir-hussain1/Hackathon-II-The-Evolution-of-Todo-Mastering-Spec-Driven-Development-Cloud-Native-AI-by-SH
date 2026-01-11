"""Authorization Matching Skill - Verify user matches resource"""

class AuthorizationMatchingSkill:
    """Validates user authorization for resource access"""

    def verify_authorization(self, token_user_id: str, route_user_id: str) -> dict:
        """
        Input:
            token_user_id: from JWT claims
            route_user_id: from URL path /api/users/{user_id}/...
        Output:
            authorized: bool
        """
        authorized = token_user_id == route_user_id

        return {
            "authorized": authorized,
            "reason": "User ID match" if authorized else "User ID mismatch",
        }

    def is_authorized(self, token_user_id: str, route_user_id: str) -> bool:
        """Quick check - returns boolean only"""
        return token_user_id == route_user_id
