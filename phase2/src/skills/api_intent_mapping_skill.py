"""API Intent Mapping Skill - Map CRUD intent to REST endpoint"""

class APIIntentMappingSkill:
    """Maps user intent to REST API endpoint"""

    def map_intent_to_endpoint(self, action_type: str) -> dict:
        """
        Input: action_type (create | read | update | delete | toggle)
        Output: {
            http_method: str,
            endpoint_pattern: str
        }
        """
        mapping = {
            "create": {
                "http_method": "POST",
                "endpoint_pattern": "/api/{user_id}/tasks",
                "body_required": True,
            },
            "read": {
                "http_method": "GET",
                "endpoint_pattern": "/api/{user_id}/tasks",
                "body_required": False,
            },
            "read_single": {
                "http_method": "GET",
                "endpoint_pattern": "/api/{user_id}/tasks/{id}",
                "body_required": False,
            },
            "update": {
                "http_method": "PUT",
                "endpoint_pattern": "/api/{user_id}/tasks/{id}",
                "body_required": True,
            },
            "delete": {
                "http_method": "DELETE",
                "endpoint_pattern": "/api/{user_id}/tasks/{id}",
                "body_required": False,
            },
            "toggle": {
                "http_method": "PATCH",
                "endpoint_pattern": "/api/{user_id}/tasks/{id}/complete",
                "body_required": False,
            },
        }

        return mapping.get(
            action_type,
            {"http_method": None, "endpoint_pattern": None, "body_required": None},
        )
