"""
JWT authentication middleware for FastAPI.
Verifies JWT tokens and enforces user_id matching.
Includes rate limiting for API endpoints.
"""
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Dict
from collections import defaultdict
from datetime import datetime, timedelta

from ..config import settings

# HTTP Bearer token security
security = HTTPBearer()


async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """
    Verify JWT token and return payload.

    Raises:
        HTTPException: If token is invalid or expired.

    Returns:
        dict: Token payload with user_id and email.
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired. Please log in again."
        )
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )


def verify_user_id_match(user_id_from_route: str, token_payload: Dict[str, str]) -> None:
    """
    Verify that user_id in route matches user_id in JWT token.

    Args:
        user_id_from_route: user_id from URL path parameter
        token_payload: Decoded JWT payload

    Raises:
        HTTPException: If user_id mismatch detected.
    """
    token_user_id = token_payload.get("sub")
    if token_user_id != user_id_from_route:
        raise HTTPException(
            status_code=403,
            detail="User ID mismatch. Access denied."
        )


async def get_current_user_id(
    user_id_from_route: str,
    token_payload: Dict[str, str] = Depends(verify_jwt)
) -> str:
    """
    Get authenticated user ID with validation.

    Usage in endpoints:
        @app.get("/api/{user_id}/resource")
        async def endpoint(
            user_id: str,
            authenticated_user_id: str = Depends(get_current_user_id)
        ):
            # authenticated_user_id is verified to match user_id
            ...

    Args:
        user_id_from_route: user_id from URL path
        token_payload: Decoded JWT payload

    Returns:
        str: Verified user_id

    Raises:
        HTTPException: If authentication fails or user_id mismatch.
    """
    verify_user_id_match(user_id_from_route, token_payload)
    return token_payload["sub"]


# ===== RATE LIMITING =====

# In-memory rate limit storage (for production, use Redis)
# Structure: {user_id: [(timestamp1, timestamp2, ...)]}
rate_limit_store: Dict[str, list] = defaultdict(list)

# Rate limit configuration
RATE_LIMIT_REQUESTS = 60  # Number of requests allowed
RATE_LIMIT_WINDOW = timedelta(minutes=1)  # Time window


def check_rate_limit(user_id: str) -> None:
    """
    Check if user has exceeded rate limit (60 requests/minute).

    Args:
        user_id: User identifier

    Raises:
        HTTPException: If rate limit exceeded
    """
    now = datetime.utcnow()
    window_start = now - RATE_LIMIT_WINDOW

    # Get user's request history
    request_times = rate_limit_store[user_id]

    # Remove requests outside the current window
    request_times[:] = [t for t in request_times if t > window_start]

    # Check if limit exceeded
    if len(request_times) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_REQUESTS} requests per minute."
        )

    # Add current request
    request_times.append(now)


async def rate_limit_middleware(user_id: str, token_payload: Dict[str, str] = Depends(verify_jwt)) -> None:
    """
    Rate limiting dependency for endpoints.

    Usage:
        @app.post("/api/{user_id}/chat")
        async def chat(
            user_id: str,
            _: None = Depends(rate_limit_middleware)
        ):
            ...

    Args:
        user_id: User ID from route
        token_payload: Decoded JWT payload

    Raises:
        HTTPException: If rate limit exceeded
    """
    # Verify user_id matches token
    verify_user_id_match(user_id, token_payload)

    # Check rate limit
    check_rate_limit(user_id)
