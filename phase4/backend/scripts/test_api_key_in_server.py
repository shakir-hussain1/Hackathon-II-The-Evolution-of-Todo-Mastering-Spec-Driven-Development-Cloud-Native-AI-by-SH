"""Test if the OpenAI API key is working."""
import asyncio
import sys

sys.path.insert(0, 'E:\\Hackathon-II-The-Evolution-of-Todo\\phase3\\backend')

from openai import AsyncOpenAI
from src.config import settings


async def test_openai_key():
    """Test OpenAI API key."""
    print(f"Testing OpenAI API key...")
    print(f"Key length: {len(settings.OPENAI_API_KEY)}")
    print(f"First 20 chars: {settings.OPENAI_API_KEY[:20]}")
    print(f"Last 10 chars: {settings.OPENAI_API_KEY[-10:]}")

    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Test with a simple completion
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'Hello' if you can hear me"}
            ],
            max_tokens=10
        )

        print(f"\n[SUCCESS] OpenAI API key is valid!")
        print(f"Response: {response.choices[0].message.content}")

    except Exception as e:
        print(f"\n[ERROR] OpenAI API key test failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_openai_key())
