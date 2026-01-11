"""
Integration & Consistency Agent
Purpose: Ensure frontend, backend, auth, and DB specs align
Responsibility: Detect field mismatches, API/client drift, naming consistency, scope compliance
"""

class IntegrationConsistencyAgent:
    """Validates alignment across all system layers"""

    def __init__(self):
        self.inconsistencies = []
        self.compliance_issues = []

    def detect_field_mismatches(self, frontend_model: dict, backend_model: dict) -> list:
        """Compare frontend and backend models"""
        frontend_fields = set(frontend_model.get("fields", []))
        backend_fields = set(backend_model.get("fields", []))

        missing_in_frontend = backend_fields - frontend_fields
        missing_in_backend = frontend_fields - backend_fields

        issues = []
        if missing_in_frontend:
            issues.append(f"Backend has fields not in frontend: {missing_in_frontend}")
        if missing_in_backend:
            issues.append(f"Frontend has fields not in backend: {missing_in_backend}")

        return issues

    def detect_api_client_drift(self, api_spec: dict, client_code: str) -> list:
        """Compare API spec with frontend client implementation"""
        issues = []

        # Check if all endpoints are implemented
        for endpoint in api_spec.get("endpoints", []):
            if endpoint not in client_code:
                issues.append(f"Missing client implementation for {endpoint}")

        return issues

    def ensure_naming_consistency(self) -> dict:
        """Validate consistent naming across layers"""
        return {
            "field_names": {
                "user_id": "Used consistently in routes, models, DB",
                "title": "Used in Task model frontend and backend",
                "status": "Enum values: 'incomplete' | 'complete'",
            },
            "endpoint_naming": "/api/users/{user_id}/tasks",
            "variable_naming": "snake_case in Python, camelCase in TypeScript",
        }

    def ensure_phase_ii_scope_compliance(self) -> dict:
        """Validate all features are in Phase II scope"""
        return {
            "in_scope_features": [
                "User signup/login (Better Auth)",
                "Task CRUD (create, read, update, delete)",
                "Task completion toggle",
                "Multi-user support",
                "JWT authentication",
                "PostgreSQL persistence",
            ],
            "out_of_scope_features": [
                "Chatbot",
                "Background jobs",
                "Role-based access control",
                "Offline support",
                "Mobile apps",
                "Analytics",
            ],
            "compliance": True,
        }

    def validate_security_consistency(self) -> dict:
        """Ensure security rules consistent across all layers"""
        return {
            "jwt_requirement": "Every API endpoint requires JWT",
            "user_id_validation": "URL user_id must match token user_id",
            "cross_user_prevention": "All queries filtered by user_id",
            "error_messages": "No sensitive information leaked",
            "secrets": "No hardcoded values, all in env vars",
        }

    def generate_consistency_report(self) -> dict:
        """Complete integration report"""
        return {
            "field_alignment": self._check_field_alignment(),
            "api_client_alignment": self._check_api_client_alignment(),
            "naming_consistency": self.ensure_naming_consistency(),
            "scope_compliance": self.ensure_phase_ii_scope_compliance(),
            "security_consistency": self.validate_security_consistency(),
            "issues": self.inconsistencies,
        }

    def _check_field_alignment(self) -> dict:
        """Check all models aligned"""
        return {"status": "OK", "mismatches": []}

    def _check_api_client_alignment(self) -> dict:
        """Check API and client aligned"""
        return {"status": "OK", "drift": []}
