"""Correlation ID middleware for distributed tracing"""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CorrelationMiddleware(BaseHTTPMiddleware):
    """Middleware to add correlation ID to all requests"""

    async def dispatch(self, request: Request, call_next):
        # Extract correlation ID from headers or generate new one
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())

        # Add to request state
        request.state.correlation_id = correlation_id

        # Call next middleware/route
        response: Response = await call_next(request)

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        return response
