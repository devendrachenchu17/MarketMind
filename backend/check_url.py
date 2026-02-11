import httpx
import asyncio
import urllib.parse

async def check():
    url = "https://pollinations.ai/p/luxury_watch?width=1000&height=1000"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            response = await client.get(url, timeout=30.0, follow_redirects=True)
            print(f"URL: {url}")
            print(f"Status: {response.status_code}")
            print(f"Type: {response.headers.get('Content-Type')}")
            if "image" in response.headers.get('Content-Type', ''):
                print("SUCCESS")
            else:
                print(f"FAILURE - Body start: {response.text[:100]}")
        except Exception as e:
            print(f"ERROR: {e}")









if __name__ == "__main__":
    asyncio.run(check())
