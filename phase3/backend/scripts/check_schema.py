"""Check database schema for users table."""
import asyncio
import sys

sys.path.insert(0, 'E:\\Hackathon-II-The-Evolution-of-Todo\\phase3\\backend')

from src.db.connection import engine


async def check_schema():
    """Check users table schema."""
    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position")
            rows = result.fetchall()

            print("\nUsers table schema:")
            print("-" * 60)
            for row in rows:
                print(f"{row[0]:<20} {row[1]:<20} nullable={row[2]}")
            print("-" * 60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_schema())
