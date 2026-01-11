"""
Authorization validation middleware and utilities.

Provides comprehensive authorization checks including:
- User_id matching between URL and JWT
- Access control verification
- Unauthorized access logging
- Fine-grained permission checking
"""

from fastapi import Request, HTTPException, status
from typing import Optional
from enum import Enum
import logging

# Setup logging for authorization events
logger = logging.getLogger(__name__)


class AuthorizationLevel(Enum):
    """Authorization levels for operations."""
    OWNER = "owner"  # User must own the resource
    AUTHENTICATED = "authenticated"  # User must be authenticated
    ADMIN = "admin"  # User must be admin (future)


def verify_ownership(
    user_id: str,
    request: Request,
    resource_owner_id: Optional[str] = None,
    operation: str = "access",
) -> bool:
    """
    Verify that authenticated user owns the resource.

    Args:
        user_id: Resource owner's user_id from database
        request: FastAPI request object
        resource_owner_id: Alternative way to pass owner_id
        operation: Description of operation (for logging)

    Returns:
        True if user is owner

    Raises:
        HTTPException: 403 Forbidden if user is not owner
    """
    # Get authenticated user_id from request state (set by middleware)
    auth_user_id = getattr(request.state, "user_id", None)

    if not auth_user_id:
        logger.warning(f"Authorization failed: no user_id in request state for {operation}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    # Compare user_id
    resource_user_id = resource_owner_id or user_id
    if auth_user_id != resource_user_id:
        logger.warning(
            f"Authorization failed: user {auth_user_id} attempted {operation} "
            f"on resource owned by {resource_user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: you do not own this resource",
        )

    logger.info(f"Authorization successful: user {auth_user_id} {operation}")
    return True


def verify_url_user_match(
    url_user_id: str,
    request: Request,
    endpoint: str = "endpoint",
) -> bool:
    """
    Verify that URL user_id matches authenticated user_id.

    This is the primary authorization check for all endpoints.

    Args:
        url_user_id: user_id from URL path parameter
        request: FastAPI request object
        endpoint: Description of endpoint (for logging)

    Returns:
        True if user_ids match

    Raises:
        HTTPException: 403 Forbidden if user_ids don't match
    """
    auth_user_id = getattr(request.state, "user_id", None)

    if not auth_user_id:
        logger.warning(f"Authorization failed: {endpoint} - no user_id in request state")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    if url_user_id != auth_user_id:
        logger.warning(
            f"Authorization failed: {endpoint} - "
            f"URL user_id={url_user_id} != auth user_id={auth_user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    logger.debug(f"Authorization successful: {endpoint} - user {auth_user_id}")
    return True


def check_authorization(
    request: Request,
    required_level: AuthorizationLevel = AuthorizationLevel.AUTHENTICATED,
    resource_owner_id: Optional[str] = None,
) -> str:
    """
    Comprehensive authorization check.

    Args:
        request: FastAPI request object
        required_level: Required authorization level
        resource_owner_id: If checking ownership, provide resource owner's user_id

    Returns:
        Authenticated user_id if authorized

    Raises:
        HTTPException: 401 if not authenticated, 403 if not authorized
    """
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    if required_level == AuthorizationLevel.AUTHENTICATED:
        # Just need to be logged in
        return user_id

    elif required_level == AuthorizationLevel.OWNER:
        # Need to own the resource
        if resource_owner_id and user_id != resource_owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: you do not own this resource",
            )
        return user_id

    elif required_level == AuthorizationLevel.ADMIN:
        # Would need admin flag on user (future implementation)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user_id


class AuthorizationValidator:
    """
    Helper class for authorization validation in route handlers.

    Usage:
        validator = AuthorizationValidator(request)
        validator.verify_user_match(url_user_id)
        validator.verify_ownership(resource.user_id)
    """

    def __init__(self, request: Request):
        """Initialize validator with request object."""
        self.request = request
        self.user_id = getattr(request.state, "user_id", None)

    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.user_id is not None

    def verify_user_match(self, url_user_id: str) -> bool:
        """Verify URL user_id matches authenticated user."""
        if not self.is_authenticated():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )

        if self.user_id != url_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: user_id mismatch",
            )

        return True

    def verify_ownership(self, resource_user_id: str) -> bool:
        """Verify authenticated user owns the resource."""
        if not self.is_authenticated():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )

        if self.user_id != resource_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: you do not own this resource",
            )

        return True

    def get_user_id(self) -> str:
        """Get authenticated user_id or raise 401."""
        if not self.is_authenticated():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        return self.user_id
