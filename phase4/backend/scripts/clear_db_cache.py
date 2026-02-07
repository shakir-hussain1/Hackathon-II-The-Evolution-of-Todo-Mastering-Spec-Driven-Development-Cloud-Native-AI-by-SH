"""Clear database connection pool."""
import asyncio
import sys

sys.path.insert(0, 'E:\\Hackathon-II-The-Evolution-of-Todo\\phase3\\backend')

from src.db.connection import engine


async def clear_cache():
    """Clear connection pool cache."""
    try:
        print("Disposing engine to clear cache...")
        await engine.dispose()
        print("[OK] Engine disposed successfully")

    except Exception as e:
        print(f"[ERROR] Failed to dispose engine: {e}")


if __name__ == "__main__":
    asyncio.run(clear_cache())
