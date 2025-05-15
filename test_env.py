import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if environment variables are loaded
mongodb_uri = os.environ.get('MONGODB_URI')
voyage_api_key = os.environ.get('VOYAGE_API_KEY')
gemini_api_key = os.environ.get('GEMINI_API_KEY')

print(f"MongoDB URI: {mongodb_uri}")
print(f"Voyage API Key: {voyage_api_key}")
print(f"Gemini API Key: {gemini_api_key}")
