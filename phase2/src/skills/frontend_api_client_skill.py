"""Frontend API Client Skill - Attach JWT to requests"""

class FrontendAPIClientSkill:
    """Defines how frontend attaches JWT to API requests"""

    def attach_jwt_to_request(self, api_request: dict, jwt_token: str) -> dict:
        """
        Input:
            api_request: {url, method, body, headers}
            jwt_token: JWT token string
        Output:
            authorized_request: request with JWT header added
        """
        if not jwt_token:
            return {
                "valid": False,
                "error": "No JWT token provided",
                "request": None,
            }

        # Add Authorization header
        authorized_request = api_request.copy()
        if "headers" not in authorized_request:
            authorized_request["headers"] = {}

        authorized_request["headers"]["Authorization"] = f"Bearer {jwt_token}"
        authorized_request["headers"]["Content-Type"] = "application/json"

        return {
            "valid": True,
            "error": None,
            "request": authorized_request,
        }

    def build_authorized_request(self, method: str, endpoint: str, jwt_token: str, body: dict = None) -> dict:
        """Quick method - build and attach JWT in one step"""
        request = {
            "method": method,
            "url": endpoint,
            "body": body,
            "headers": {
                "Authorization": f"Bearer {jwt_token}",
                "Content-Type": "application/json",
            },
        }
        return request
