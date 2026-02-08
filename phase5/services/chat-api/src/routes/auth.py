"""Authentication routes for user registration and login"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.auth_service import AuthService
from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from ..middleware.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.

    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 8 characters)
    - **full_name**: Optional full name
    - **timezone**: IANA timezone (default: UTC)

    Returns JWT access token on successful registration.
    """
    auth_service = AuthService(db)

    try:
        # Register user
        user = auth_service.register_user(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            timezone=request.timezone
        )

        # Create token
        token = auth_service.create_token_for_user(user)

        return TokenResponse(**token)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.

    - **email**: User email address
    - **password**: User password

    Returns JWT access token on successful authentication.
    """
    auth_service = AuthService(db)

    # Authenticate user
    user = auth_service.authenticate_user(request.email, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create token
    token = auth_service.create_token_for_user(user)

    return TokenResponse(**token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's information.

    Requires valid JWT token in Authorization header.
    """
    return UserResponse(**current_user.to_dict())
