"""Test auth endpoint directly."""
import asyncio
import sys
import uuid

sys.path.insert(0, 'E:\\Hackathon-II-The-Evolution-of-Todo\\phase3\\backend')

from src.api.auth import RegisterRequest, register
from src.db.connection import async_session_maker


async def test_registration():
    """Test registration endpoint."""
    print("Testing registration endpoint...")

    try:
        # Create test request
        request = RegisterRequest(
            email=f"test_{uuid.uuid4().hex[:8]}@example.com",
            password="password123"
        )

        print(f"Request email: {request.email}")
        print(f"Request password: {request.password}")

        # Call register function
        async with async_session_maker() as session:
            result = await register(request, session)

            print(f"[SUCCESS] Registration successful!")
            print(f"User ID: {result.user['id']}")
            print(f"User Email: {result.user['email']}")
            print(f"Token (first 50 chars): {result.token[:50]}")

    except Exception as e:
        print(f"[ERROR] Registration failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_registration())
