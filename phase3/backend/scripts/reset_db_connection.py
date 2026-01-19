"""Reset database connection and clear all caches."""
import asyncio
import sys

sys.path.insert(0, 'E:\\Hackathon-II-The-Evolution-of-Todo\\phase3\\backend')

from sqlalchemy import text
from src.db.connection import engine


async def reset_connection():
    """Reset database connection."""
    try:
        # Dispose existing connections
        await engine.dispose()
        print("Engine disposed")

        # Create new connection with autocommit and execute DISCARD ALL
        async with engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT").execute(text("DISCARD ALL"))
            print("Executed DISCARD ALL")

        # Dispose again to ensure clean state
        await engine.dispose()
        print("[OK] Database connection reset successfully")

    except Exception as e:
        print(f"[ERROR] Failed to reset connection: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(reset_connection())
