from app.utils.llm_client import llm_client
import asyncio
import os

async def test():
    prompt = "Luxury gold watch on a black background"
    print(f"Testing generate_image with prompt: {prompt}")
    url = await llm_client.generate_image(prompt)
    print(f"Generated URL: {url}")
    
    # Try an LLM call too
    messages = [{"role": "user", "content": "Product: Watch"}]
    print("Testing generate...")
    llm_res = await llm_client.generate(messages)
    print(f"LLM Response: {llm_res[:100]}...")

if __name__ == "__main__":
    asyncio.run(test())
