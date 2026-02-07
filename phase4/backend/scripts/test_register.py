"""Test registration directly to see the actual error."""
import asyncio
import sys
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

# Add src to path
sys.path.insert(0, 'E:\\Hackathon-II-The-Evolution-of-Todo\\phase3\\backend')

from src.models import User
from src.api.auth import hash_password
from src.db.connection import async_session_maker


async def test_register():
    """Test user registration."""
    print("Testing user registration...")

    try:
        async with async_session_maker() as session:
            # Create test user
            test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
            test_password = "test123"

            print(f"Creating user with email: {test_email}")

            # Check if user exists
            result = await session.exec(select(User).where(User.email == test_email))
            existing_user = result.first()

            if existing_user:
                print("User already exists")
                return

            # Create new user
            user = User(
                id=str(uuid.uuid4()),
                email=test_email,
                password_hash=hash_password(test_password)
            )

            print(f"User object created: {user.id}, {user.email}")

            session.add(user)
            await session.commit()
            await session.refresh(user)

            print(f"[SUCCESS] User created: {user.id}, {user.email}")

    except Exception as e:
        print(f"[ERROR] Registration failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_register())
