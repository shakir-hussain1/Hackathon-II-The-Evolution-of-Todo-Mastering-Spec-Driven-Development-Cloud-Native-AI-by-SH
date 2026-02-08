"""Authentication service for user registration and login"""

import uuid
from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import User
from ..middleware.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.logging import get_logger

logger = get_logger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for user authentication and registration"""

    def __init__(self, db: Session):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify plain password against hashed password"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a plain password"""
        return pwd_context.hash(password)

    def register_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        timezone: str = "UTC"
    ) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user
        user = User(
            email=email,
            password_hash=self.get_password_hash(password),
            full_name=full_name,
            timezone=timezone,
            notification_preferences={"email": True, "push": False}
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info(f"User registered: {user.email} (ID: {user.id})")
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.db.query(User).filter(
            User.email == email,
            User.deleted_at == None
        ).first()

        if not user:
            logger.warning(f"Authentication failed: user not found - {email}")
            return None

        if not self.verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: invalid password - {email}")
            return None

        logger.info(f"User authenticated: {user.email} (ID: {user.id})")
        return user

    def create_token_for_user(self, user: User) -> dict:
        """Create JWT access token for user"""
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
        }

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(
            User.id == user_id,
            User.deleted_at == None
        ).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(
            User.email == email,
            User.deleted_at == None
        ).first()
