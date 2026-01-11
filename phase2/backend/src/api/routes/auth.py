"""
Authentication routes - signup, login, logout.

Handles user registration and authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
import jwt
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext

from src.db.database import get_session
from src.db.models import User
from src.config import settings


# Request models
class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(user_id: str) -> str:
    """
    Create a JWT token for a user.

    Args:
        user_id: User's unique identifier

    Returns:
        JWT token string
    """
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token


@router.post("/signup")
async def signup(
    req: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Create a new user account.

    Args:
        req: SignupRequest with email and password
        session: Database session

    Returns:
        dict with user_id and JWT token

    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == req.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(req.password)

    user = User(
        id=user_id,
        email=req.email,
        password_hash=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate JWT token
    token = create_jwt_token(user_id)

    return {
        "success": True,
        "user": {
            "id": user.id,
            "email": user.email,
        },
        "token": token,
    }


@router.post("/login")
async def login(
    req: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate a user and return JWT token.

    Args:
        req: LoginRequest with email and password
        session: Database session

    Returns:
        dict with user_id and JWT token

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == req.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_jwt_token(user.id)

    return {
        "success": True,
        "user": {
            "id": user.id,
            "email": user.email,
        },
        "token": token,
    }


@router.post("/logout")
async def logout():
    """
    Logout endpoint.

    Note: JWT tokens are stateless, so logout is just a frontend operation
    (clear token from localStorage). This endpoint can be used for audit logging.

    Returns:
        dict with success message
    """
    return {
        "success": True,
        "message": "Logged out successfully"
    }
