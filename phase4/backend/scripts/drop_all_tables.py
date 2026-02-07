"""Drop all tables including dependencies."""
import asyncio
import sys

sys.path.insert(0, 'E:\\Hackathon-II-The-Evolution-of-Todo\\phase3\\backend')

from sqlalchemy import text
from src.db.connection import engine


async def drop_all_tables():
    """Drop all tables using CASCADE."""
    try:
        async with engine.begin() as conn:
            print("Dropping all tables...")

            # Get all table names
            result = await conn.execute(text("""
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]

            print(f"Found tables: {tables}")

            # Drop each table with CASCADE
            for table in tables:
                print(f"Dropping table: {table}")
                await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))

            print("[OK] All tables dropped successfully")

        await engine.dispose()

    except Exception as e:
        print(f"[ERROR] Failed to drop tables: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(drop_all_tables())
