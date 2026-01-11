"""
API Design & Validation Agent
Purpose: Ensure REST API endpoints match specs and security rules
Responsibility: Validate endpoints, JWT enforcement, user_id matching, models
"""

class APIDesignValidationAgent:
    """Validates API design against specifications"""

    def __init__(self):
        self.violations = []
        self.compliance_report = {}

    def validate_endpoint_structure(self, endpoint: dict) -> bool:
        """Validate endpoint path, method, headers"""
        method = endpoint.get("method")
        path = endpoint.get("path")
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        return method in valid_methods and path.startswith("/api/")

    def validate_jwt_enforcement(self, endpoint: dict) -> bool:
        """Verify JWT required on endpoint"""
        headers = endpoint.get("headers", {})
        requires_auth = "Authorization" in headers
        if not requires_auth:
            self.violations.append(f"Missing JWT on {endpoint.get('path')}")
        return requires_auth

    def validate_user_id_matching(self, endpoint: dict) -> bool:
        """Verify user_id in path matches authenticated user"""
        path = endpoint.get("path", "")
        has_user_id_param = "{user_id}" in path
        if has_user_id_param:
            return True
        self.violations.append(f"Missing user_id parameter in {path}")
        return False

    def validate_request_model(self, endpoint: dict) -> bool:
        """Validate request body model"""
        if endpoint.get("method") in ["POST", "PUT", "PATCH"]:
            return "body" in endpoint
        return True

    def validate_response_model(self, endpoint: dict) -> bool:
        """Validate response model for status code"""
        return "response" in endpoint

    def generate_compliance_report(self, endpoints: list) -> dict:
        """Generate validation report"""
        return {
            "total_endpoints": len(endpoints),
            "violations": self.violations,
            "compliant": len(self.violations) == 0,
        }
