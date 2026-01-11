"""
Backend Architecture Agent
Purpose: Reason about FastAPI + SQLModel backend design
Responsibility: Validate model-schema alignment, route separation, user-filtered queries, error-handling conventions
"""

class BackendArchitectureAgent:
    """Reasons about FastAPI backend architecture"""

    def __init__(self):
        self.models = {}
        self.routes = {}
        self.data_ownership_rules = []

    def validate_model_to_schema_alignment(self) -> dict:
        """Ensure Pydantic models match SQLModel schema"""
        return {
            "User": {
                "sqlmodel": ["id", "email", "name", "created_at"],
                "pydantic": ["id", "email", "name", "created_at"],
                "aligned": True,
            },
            "Task": {
                "sqlmodel": ["id", "user_id", "title", "description", "status", "created_at", "updated_at"],
                "pydantic": ["id", "user_id", "title", "description", "status", "created_at", "updated_at"],
                "aligned": True,
            },
        }

    def validate_route_separation(self) -> dict:
        """Organize routes by concern"""
        return {
            "/api/users/{user_id}/tasks": {
                "module": "routes/tasks.py",
                "methods": ["GET", "POST"],
                "auth_required": True,
            },
            "/api/users/{user_id}/tasks/{id}": {
                "module": "routes/tasks.py",
                "methods": ["GET", "PUT", "DELETE", "PATCH"],
                "auth_required": True,
            },
        }

    def ensure_user_filtered_queries(self) -> dict:
        """Database queries must filter by user_id"""
        return {
            "rule": "All Task queries must include WHERE user_id = authenticated_user_id",
            "examples": [
                "SELECT * FROM tasks WHERE user_id = ? AND id = ?",
                "UPDATE tasks SET title = ? WHERE user_id = ? AND id = ?",
                "DELETE FROM tasks WHERE user_id = ? AND id = ?",
            ],
            "enforcement": "Add user_id parameter to every query",
        }

    def enforce_error_handling_conventions(self) -> dict:
        """Standardized error responses"""
        return {
            "400": {"message": "Invalid input", "example": "Title cannot be empty"},
            "401": {"message": "Unauthorized", "example": "Missing or invalid JWT token"},
            "403": {"message": "Forbidden", "example": "User ID mismatch"},
            "404": {"message": "Not found", "example": "Task does not exist"},
            "500": {"message": "Server error", "example": "Database connection failed"},
        }

    def define_service_layer_pattern(self) -> dict:
        """Service layer for business logic"""
        return {
            "location": "/backend/src/services/",
            "modules": {
                "task_service.py": [
                    "create_task(user_id, title, description)",
                    "get_user_tasks(user_id, status_filter)",
                    "update_task(user_id, task_id, title, description)",
                    "delete_task(user_id, task_id)",
                    "toggle_task(user_id, task_id)",
                ],
            },
        }

    def define_middleware_requirements(self) -> dict:
        """Middleware for auth, logging, error handling"""
        return {
            "jwt_middleware": "Verify JWT token on every request",
            "user_id_validation": "Validate user_id in path matches token",
            "error_handler": "Catch exceptions and return standardized responses",
            "logging": "Log all requests with timestamp and user_id",
        }

    def generate_architecture_plan(self) -> dict:
        """Complete backend architecture"""
        return {
            "model_alignment": self.validate_model_to_schema_alignment(),
            "routes": self.validate_route_separation(),
            "data_ownership": self.ensure_user_filtered_queries(),
            "error_handling": self.enforce_error_handling_conventions(),
            "services": self.define_service_layer_pattern(),
            "middleware": self.define_middleware_requirements(),
        }
