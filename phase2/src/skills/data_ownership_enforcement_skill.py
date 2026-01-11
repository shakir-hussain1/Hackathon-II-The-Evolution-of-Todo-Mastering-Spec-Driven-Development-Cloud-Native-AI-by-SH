"""Data Ownership Enforcement Skill - Scope queries to user"""

class DataOwnershipEnforcementSkill:
    """Ensures all operations are scoped to authenticated user"""

    def generate_filtered_query_rules(self, user_id: str, query_context: str) -> dict:
        """
        Input:
            user_id: authenticated user
            query_context: type of query (list_tasks, get_task, update_task, delete_task)
        Output:
            filtered_query_rules: dict with WHERE clause rules
        """
        rules = {
            "list_tasks": {
                "where_clause": f"WHERE user_id = '{user_id}'",
                "sql_template": f"SELECT * FROM tasks WHERE user_id = ? AND status = ?",
            },
            "get_task": {
                "where_clause": f"WHERE user_id = '{user_id}' AND id = ?",
                "sql_template": f"SELECT * FROM tasks WHERE user_id = ? AND id = ?",
            },
            "update_task": {
                "where_clause": f"WHERE user_id = '{user_id}' AND id = ?",
                "sql_template": f"UPDATE tasks SET title = ?, description = ? WHERE user_id = ? AND id = ?",
            },
            "delete_task": {
                "where_clause": f"WHERE user_id = '{user_id}' AND id = ?",
                "sql_template": f"DELETE FROM tasks WHERE user_id = ? AND id = ?",
            },
            "toggle_task": {
                "where_clause": f"WHERE user_id = '{user_id}' AND id = ?",
                "sql_template": f"UPDATE tasks SET status = ? WHERE user_id = ? AND id = ?",
            },
        }

        return rules.get(
            query_context,
            {"where_clause": f"WHERE user_id = '{user_id}'", "sql_template": None},
        )

    def enforce_ownership(self, user_id: str) -> str:
        """Quick enforcement - returns WHERE clause only"""
        return f"WHERE user_id = '{user_id}'"
