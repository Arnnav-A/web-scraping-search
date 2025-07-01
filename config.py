import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "mixtral-8x7b-32768")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY environment variable.")
