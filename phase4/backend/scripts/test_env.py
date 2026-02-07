"""
Diagnostic script to test environment configuration.
Run this to verify all credentials are loaded correctly.
"""
import os
import sys

print("=" * 60)
print("PHASE III - Environment Diagnostics")
print("=" * 60)

# Test 1: Check .env file exists
print("\n1. Checking .env file...")
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    print(f"   ✅ .env file found at: {env_path}")
    with open(env_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    print(f"   📝 .env has {len(lines)} configuration lines")
else:
    print(f"   ❌ .env file NOT FOUND at: {env_path}")
    print(f"   ⚠️  Create .env file by copying .env.example")
    sys.exit(1)

# Test 2: Load dotenv
print("\n2. Loading python-dotenv...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("   ✅ python-dotenv loaded successfully")
except ImportError:
    print("   ❌ python-dotenv not installed")
    print("   Run: pip install python-dotenv")
    sys.exit(1)

# Test 3: Check environment variables
print("\n3. Checking environment variables...")

def check_env_var(name, show_value=False, min_length=0):
    value = os.getenv(name)
    if value:
        if show_value:
            # Show partial value for debugging
            if len(value) > 50:
                display = value[:30] + "..." + value[-10:]
            else:
                display = value
            print(f"   ✅ {name}: {display}")
        else:
            print(f"   ✅ {name}: SET (length={len(value)})")

        if min_length and len(value) < min_length:
            print(f"      ⚠️  Warning: Value seems too short (expected >{min_length} chars)")
            return False
        return True
    else:
        print(f"   ❌ {name}: MISSING")
        return False

all_good = True
all_good &= check_env_var("DATABASE_URL", show_value=True, min_length=30)
all_good &= check_env_var("OPENAI_API_KEY", show_value=False, min_length=40)
all_good &= check_env_var("JWT_SECRET", show_value=False, min_length=16)
check_env_var("JWT_ALGORITHM", show_value=True)
check_env_var("JWT_EXPIRATION_HOURS", show_value=True)
check_env_var("ENVIRONMENT", show_value=True)
check_env_var("DEBUG", show_value=True)
check_env_var("CORS_ORIGINS", show_value=True)

# Test 4: Validate DATABASE_URL format
print("\n4. Validating DATABASE_URL format...")
db_url = os.getenv("DATABASE_URL", "")
if db_url:
    if db_url.startswith("postgresql+asyncpg://"):
        print("   ✅ DATABASE_URL has correct driver (asyncpg)")
    elif db_url.startswith("postgresql://"):
        print("   ⚠️  DATABASE_URL uses 'postgresql://' instead of 'postgresql+asyncpg://'")
        print("      Change it to: postgresql+asyncpg://...")
    else:
        print(f"   ❌ DATABASE_URL has wrong format: {db_url[:30]}...")
        print("      Should start with: postgresql+asyncpg://")
        all_good = False

# Test 5: Test OpenAI API
print("\n5. Testing OpenAI API key...")
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    if api_key.startswith("sk-proj-") or api_key.startswith("sk-"):
        print(f"   ✅ API key format looks correct: {api_key[:15]}...")

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            models = client.models.list()
            print(f"   ✅ OpenAI API key is VALID! ({len(models.data)} models available)")
        except Exception as e:
            print(f"   ❌ OpenAI API test FAILED: {str(e)}")
            all_good = False
    else:
        print(f"   ⚠️  API key format unusual: {api_key[:20]}...")
        print("      Expected format: sk-proj-... or sk-...")

# Test 6: Test database connection
print("\n6. Testing database connection...")
if db_url:
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        import asyncio

        engine = create_async_engine(db_url, echo=False)

        async def test_connection():
            async with engine.begin() as conn:
                await conn.exec_driver_sql("SELECT 1")
            await engine.dispose()

        asyncio.run(test_connection())
        print("   ✅ Database connection successful!")
    except Exception as e:
        print(f"   ❌ Database connection FAILED: {str(e)}")
        all_good = False

# Test 7: Check Python version
print("\n7. Checking Python version...")
python_version = sys.version_info
print(f"   Python {python_version.major}.{python_version.minor}.{python_version.micro}")
if python_version.major == 3 and python_version.minor >= 10:
    print("   ✅ Python version compatible")
else:
    print("   ⚠️  Recommended Python 3.10+")

# Final summary
print("\n" + "=" * 60)
if all_good:
    print("✅ ALL CHECKS PASSED - Ready to start!")
    print("\nRun the application:")
    print("   uvicorn src.main:app --reload")
else:
    print("❌ SOME CHECKS FAILED - Fix issues above")
    print("\nCommon fixes:")
    print("   1. Check .env file has correct values (no quotes, no spaces)")
    print("   2. Verify DATABASE_URL starts with 'postgresql+asyncpg://'")
    print("   3. Verify OpenAI API key is correct and has billing enabled")
    print("   4. Run: pip install -r requirements.txt")
print("=" * 60)
