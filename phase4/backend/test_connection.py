"""
Quick test script to verify database connection works.
Run this before starting the server to catch configuration issues.
"""
import asyncio
from src.db.connection import init_db, close_db, engine
from src.config import settings

async def test_connection():
    print("=" * 60)
    print("Testing Backend Configuration")
    print("=" * 60)

    print(f"\n1. Configuration Check:")
    print(f"   DATABASE_URL: {settings.DATABASE_URL}")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   ENVIRONMENT: {settings.ENVIRONMENT}")

    print(f"\n2. Engine Check:")
    print(f"   Engine created: {engine is not None}")
    print(f"   Engine type: {type(engine).__name__}")

    try:
        print(f"\n3. Database Initialization:")
        print(f"   Initializing database...")
        await init_db()
        print(f"   ✓ Database initialized successfully!")
        print(f"   ✓ Tables created!")

        print(f"\n4. Connection Test:")
        print(f"   Testing connection...")
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            print(f"   ✓ Connection successful!")

        print(f"\n5. Cleanup:")
        await close_db()
        print(f"   ✓ Connection closed!")

        print(f"\n" + "=" * 60)
        print("✓ ALL TESTS PASSED - Backend is ready to start!")
        print("=" * 60)

    except Exception as e:
        print(f"\n" + "=" * 60)
        print(f"✗ ERROR: {type(e).__name__}")
        print(f"✗ Message: {str(e)}")
        print("=" * 60)
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())
