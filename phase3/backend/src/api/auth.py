"""
Authentication endpoints using Better Auth pattern with JWT.
Provides user registration and login with JWT token generation.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import uuid

from ..config import settings
from ..models import User
from ..db.connection import get_session

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Router
router = APIRouter(prefix="/auth", tags=["Authentication"])


# Request/Response models
class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Authentication response with user and token."""
    user: dict
    token: str


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(user_id: str, email: str) -> str:
    """Create JWT token for authenticated user."""
    payload = {
        "sub": user_id,
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


@router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    """Register a new user account."""
    # Check if user exists
    result = await session.execute(select(User).where(User.email == request.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        password_hash=hash_password(request.password)
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate JWT token
    token = create_jwt_token(user.id, user.email)

    return AuthResponse(
        user={"id": user.id, "email": user.email},
        token=token
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """Login with email and password."""
    # Find user
    result = await session.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token = create_jwt_token(user.id, user.email)

    return AuthResponse(
        user={"id": user.id, "email": user.email},
        token=token
    )
