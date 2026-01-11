"""
Frontend Architecture Agent
Purpose: Reason about Next.js App Router architecture from specs
Responsibility: Map UI specs to pages/components, API client pattern, server vs client components, auth-aware rendering
"""

class FrontendArchitectureAgent:
    """Reasons about Next.js frontend architecture"""

    def __init__(self):
        self.page_mapping = {}
        self.component_mapping = {}
        self.data_fetching_strategy = {}

    def map_ui_specs_to_pages(self) -> dict:
        """Map spec requirements to Next.js pages"""
        return {
            "/": "Landing page (redirects to /auth if not logged in, /dashboard if logged in)",
            "/auth/signup": "Signup page with Better Auth form",
            "/auth/login": "Login page with Better Auth form",
            "/dashboard": "Main task dashboard (protected route)",
            "/tasks/[id]/edit": "Edit task page (protected route)",
        }

    def map_ui_specs_to_components(self) -> dict:
        """Map UI components from specs"""
        return {
            "TaskList": "Displays all tasks with status indicators",
            "TaskItem": "Single task row with edit/delete/toggle buttons",
            "TaskForm": "Create/edit task form with validation",
            "AuthGuard": "Wrapper component for protected routes",
            "Header": "Navigation, user info, logout button",
            "ErrorBoundary": "Error handling and display",
        }

    def enforce_api_client_usage(self) -> dict:
        """Define API client pattern"""
        return {
            "pattern": "Custom fetch wrapper with JWT attachment",
            "location": "/frontend/src/utils/api-client.ts",
            "responsibilities": [
                "Add Authorization header with JWT",
                "Handle 401 responses (redirect to login)",
                "Handle 403 responses (permission denied)",
                "Handle 404 responses (not found)",
                "Retry logic for transient failures",
            ],
        }

    def distinguish_server_vs_client_components(self) -> dict:
        """Identify which components are server vs client"""
        return {
            "server_components": [
                "Layout (app layout wrapper)",
                "ProtectedLayout (dashboard wrapper)",
            ],
            "client_components": [
                "TaskList (state management)",
                "TaskForm (form interactivity)",
                "Header (user interaction)",
                "AuthGuard (conditional rendering)",
            ],
        }

    def ensure_auth_aware_ui_rendering(self) -> dict:
        """Define auth-aware rendering logic"""
        return {
            "rules": [
                "If no JWT token in storage → Show login page",
                "If JWT token expired → Show login page + redirect",
                "If user authenticated → Show dashboard",
                "If 403 error → Show permission denied message",
                "If API fails → Show retry button",
            ],
        }

    def generate_architecture_plan(self) -> dict:
        """Complete frontend architecture"""
        return {
            "pages": self.map_ui_specs_to_pages(),
            "components": self.map_ui_specs_to_components(),
            "api_client": self.enforce_api_client_usage(),
            "component_types": self.distinguish_server_vs_client_components(),
            "auth_rendering": self.ensure_auth_aware_ui_rendering(),
        }
