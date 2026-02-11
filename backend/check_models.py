import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

with open("model_list.txt", "w") as f:
    if not api_key:
        f.write("Error: GEMINI_API_KEY not found in .env\n")
    else:
        genai.configure(api_key=api_key)
        try:
            f.write("Available models:\n")
            for m in genai.list_models():
                f.write(f"- {m.name} (Methods: {m.supported_generation_methods})\n")
        except Exception as e:
            f.write(f"Error listing models: {e}\n")
