"""
JWT authentication middleware.

Validates JWT tokens on every API request and extracts user_id from claims.
"""

import jwt
from jwt import PyJWTError
from fastapi import Request, HTTPException, status
from src.config import settings
from typing import Optional


def extract_token(request: Request) -> Optional[str]:
    """
    Extract JWT token from Authorization header.

    Expected format: Authorization: Bearer <token>

    Args:
        request: FastAPI request object

    Returns:
        Token string or None if not present
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:]  # Remove "Bearer " prefix


def verify_token(token: str) -> dict:
    """
    Verify JWT signature and extract claims.

    Raises HTTPException with 401 status if token is invalid or expired.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload (dict)

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def auth_middleware(request: Request, call_next):
    """
    Middleware to validate JWT on all protected endpoints.

    Public endpoints (signup, login) skip JWT validation.
    Protected endpoints require valid JWT with matching user_id in URL.

    Attaches user_id to request.state for use in route handlers.

    Args:
        request: FastAPI request object
        call_next: Next middleware/handler

    Returns:
        Response object

    Raises:
        HTTPException: If JWT is missing, invalid, expired, or user_id mismatches
    """
    from fastapi.responses import JSONResponse

    # CORS headers to add to all responses (including errors)
    cors_headers = {
        "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
    }

    # Skip OPTIONS requests (CORS preflight) - handle immediately
    if request.method == "OPTIONS":
        return JSONResponse(content={}, headers=cors_headers)

    # Public endpoints that skip JWT validation
    public_paths = [
        "/auth/signup",
        "/auth/login",
        "/auth/logout",
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
    ]

    # Check if this is a public endpoint
    if any(request.url.path.startswith(path) for path in public_paths):
        response = await call_next(request)
        # Add CORS headers to public endpoint responses too
        for key, value in cors_headers.items():
            response.headers[key] = value
        return response

    # Extract token from Authorization header
    token = extract_token(request)
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "error": "unauthorized",
                "message": "Missing authorization token"
            },
            headers={**cors_headers, "WWW-Authenticate": "Bearer"},
        )

    # Verify token and extract claims
    try:
        payload = verify_token(token)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "error": "unauthorized",
                "message": e.detail
            },
            headers={**cors_headers, **e.headers} if e.headers else cors_headers,
        )

    user_id = payload.get("sub")  # "sub" claim contains user_id

    if not user_id:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "error": "unauthorized",
                "message": "Invalid token claims: missing user_id"
            },
            headers=cors_headers,
        )

    # Verify route user_id matches JWT user_id
    # Path params format: /api/users/{user_id}/tasks
    route_user_id = request.path_params.get("user_id")
    if route_user_id and route_user_id != user_id:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "success": False,
                "error": "forbidden",
                "message": "Access denied: user_id mismatch"
            },
            headers=cors_headers,
        )

    # Attach user_id to request state for use in route handlers
    request.state.user_id = user_id

    # Continue to next middleware/handler
    response = await call_next(request)

    # Add CORS headers to successful responses
    for key, value in cors_headers.items():
        response.headers[key] = value

    return response
