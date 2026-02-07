"""Simple test without Unicode characters for Windows compatibility."""
import asyncio
from src.db.connection import init_db, close_db
from src.config import settings

async def test():
    print("="  * 60)
    print("Backend Configuration Test")
    print("=" * 60)
    print(f"Database: {settings.DATABASE_URL}")
    print(f"Debug: {settings.DEBUG}")

    try:
        print("\nInitializing database...")
        await init_db()
        print("SUCCESS: Database initialized and tables created!")

        await close_db()
        print("SUCCESS: Connection closed!")

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED - Backend ready to start!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\nERROR: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test())
    exit(0 if success else 1)
