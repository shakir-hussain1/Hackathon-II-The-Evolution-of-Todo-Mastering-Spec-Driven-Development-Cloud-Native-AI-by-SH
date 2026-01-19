"""
MCP server initialization using Official MCP SDK.
Provides stateless tool execution for AI agent.
"""
from mcp.server import Server
from typing import Optional

# Global MCP server instance
_mcp_server: Optional[Server] = None


def get_mcp_server() -> Server:
    """
    Get or create MCP server instance.
    Server is stateless and tools are registered on first access.
    """
    global _mcp_server

    if _mcp_server is None:
        _mcp_server = Server("phase3-todo-mcp-server")
        # Tools will be registered via decorators in tools.py
        from . import tools  # noqa: F401 - Import to register decorated tools

    return _mcp_server


def reset_mcp_server():
    """Reset MCP server (for testing)."""
    global _mcp_server
    _mcp_server = None
