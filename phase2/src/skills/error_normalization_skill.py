"""Error Normalization Skill - Convert errors to safe client messages"""

class ErrorNormalizationSkill:
    """Converts backend/auth errors into safe user messages"""

    def normalize_error(self, error_object: dict) -> dict:
        """
        Input: error_object with error_type and details
        Output: {
            user_safe_message: str,
            http_status_code: int
        }
        """
        error_type = error_object.get("type")
        error_detail = error_object.get("detail")

        mapping = {
            "validation_error": {
                "user_safe_message": "Invalid input. Please check your entries.",
                "http_status_code": 400,
            },
            "jwt_expired": {
                "user_safe_message": "Your session has expired. Please log in again.",
                "http_status_code": 401,
            },
            "jwt_invalid": {
                "user_safe_message": "Authentication failed. Please log in again.",
                "http_status_code": 401,
            },
            "user_id_mismatch": {
                "user_safe_message": "You do not have permission to access this resource.",
                "http_status_code": 403,
            },
            "task_not_found": {
                "user_safe_message": "Task not found. It may have been deleted.",
                "http_status_code": 404,
            },
            "database_error": {
                "user_safe_message": "A server error occurred. Please try again later.",
                "http_status_code": 500,
            },
            "network_error": {
                "user_safe_message": "Network error. Please check your connection.",
                "http_status_code": 500,
            },
        }

        return mapping.get(
            error_type,
            {
                "user_safe_message": "An unexpected error occurred.",
                "http_status_code": 500,
            },
        )
