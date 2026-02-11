import os
import httpx
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Ensure environment variables are loaded immediately
load_dotenv()
print(f"DEBUG: Loaded env keys: {[k for k in os.environ.keys() if 'API_KEY' in k]}")

class LLMClient:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self.api_key = os.getenv(f"{provider.upper()}_API_KEY")
        
        # Check if the key is a placeholder or empty
        if self.api_key and isinstance(self.api_key, str) and "your_" in self.api_key.lower():
            self.api_key = None

            
        print(f"LLMClient initialized with provider: {provider}. API Key loaded: {'Yes' if self.api_key else 'No'}")
        
        # Default to Groq for now
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    async def generate(self, messages: List[Dict[str, str]], model: str = "", temperature: float = 0.7) -> str:

        # Check for Gemini first if key exists
        gemini_key = os.getenv("GEMINI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        
        # Extract product for Dynamic Mock if AI fails
        product_name = "Product"
        for m in reversed(messages):
            if "Product:" in m["content"]:
                product_name = m["content"].split("Product:")[1].split(",")[0].strip()
                break
            elif "product is" in m["content"].lower():
                product_name = m["content"].lower().split("product is")[1].strip().split()[0]
                break

        # Helper for Mock (Dynamic)
        def get_mock_response(prod):
            import random
            return json.dumps({
                "strategy_explanation": f"DEMO MODE: Insights for {prod}.",
                "generated_content": [], # Empty for generic
                "variants": [
                    {
                        "variant_type": "Cold Email",
                        "subject_line": f"Solving {prod} challenges",
                        "content": f"Hi, I noticed you're working with {prod}. We help teams optimize this.",
                        "xai_explanation": "Direct value prop."
                    }
                ],
                "score": 85,
                "priority": "High"
            })


        # --- TRY GEMINI ---
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                
                # Using the exact names from model_list.txt for maximum compatibility
                models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]
                
                for m_name in models_to_try:
                    try:
                        print(f"DEBUG: Attempting Gemini {m_name}")
                        model_instance = genai.GenerativeModel(m_name)
                        system_instruction = next((m["content"] for m in messages if m["role"] == "system"), "")
                        user_message = next((m["content"] for m in messages if m["role"] == "user"), "")
                        full_prompt = f"System: {system_instruction}\n\nUser: {user_message}\n\nJSON Output:"
                        
                        # Use JSON mode if available
                        generation_config = {"response_mime_type": "application/json"}
                        response = await model_instance.generate_content_async(full_prompt, generation_config=generation_config)
                        text = response.text

                        if "{" in text:
                            return text[text.find("{"):text.rfind("}")+1]
                        return text
                    except Exception as e:
                        print(f"DEBUG: Gemini {m_name} failed: {e}")
                        continue
            except Exception as e:
                print(f"DEBUG: Gemini setup failed: {e}")

        # --- TRY GROQ ---
        if groq_key:
            try:
                import httpx
                headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                data = {
                    "model": "llama-3.1-8b-instant", 
                    "messages": messages,
                    "temperature": temperature
                }
                async with httpx.AsyncClient() as client:
                    response = await client.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers, timeout=20.0)
                    if response.status_code == 200:
                        raw_res = response.json()['choices'][0]['message']['content']
                        print(f"DEBUG: Groq raw response: {raw_res[:200]}...")
                        return raw_res
            except Exception as e:
                print(f"DEBUG: Groq fallback failed: {e}")

        print("DEBUG: Using mock response")
        return get_mock_response(product_name)


    async def generate_image(self, prompt: str, aspect_ratio: str = "1:1") -> str:
        """
        Generates an image using Pollinations.ai with a fallback to Picsum.
        """
        import urllib.parse
        import random
        
        # Clean prompt: ONLY alphanumeric and spaces, then replace spaces with underscores
        # Pollinations often handles underscores better for direct links
        clean_prompt = "".join(c for c in prompt if c.isalnum() or c == " ")
        
        # Add style modifiers if not present
        if len(clean_prompt.split()) < 5:
            clean_prompt = f"Professional studio photography of {clean_prompt}, high resolution, 4k, crisp details, white background"
        
        url_prompt = clean_prompt.strip().replace(" ", "_")
        if len(url_prompt) > 200:
            url_prompt = url_prompt[0:200]


        
        width, height = 1024, 1024
        if aspect_ratio == "9:16": width, height = 768, 1344
        seed = random.randint(0, 999999)
        
        # Format 1: Direct link
        image_url = f"https://pollinations.ai/p/{url_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
        
        print(f"DEBUG: Generated Image URL: {image_url}")
        return image_url


    async def generate_video(self, prompt: str, aspect_ratio: str = "1:1") -> str:
        import random
        stock_videos = ["https://cdn.coverr.co/videos/coverr-typing-on-a-macbook-4734/1080p.mp4", "https://cdn.coverr.co/videos/coverr-working-on-a-laptop-4503/1080p.mp4"]
        return random.choice(stock_videos)

llm_client = LLMClient(provider="gemini")
