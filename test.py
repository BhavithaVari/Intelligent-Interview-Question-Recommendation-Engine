import os
from dotenv import load_dotenv

load_dotenv()

print(f"Current directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")
print(f"GROQ_API_KEY exists: {bool(os.getenv('GROQ_API_KEY'))}")

try:
    from groq import Groq
    print("✅ Groq imported successfully")
except ImportError:
    print("❌ Groq not installed")  