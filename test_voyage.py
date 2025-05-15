import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.environ.get('VOYAGE_API_KEY')
print(f"API key: {api_key}")

# Test imports from voyageai
try:
    import voyageai
    print("Successfully imported voyageai")
    print(f"voyageai version: {voyageai.__version__}")
    print(f"Available attributes and methods in voyageai: {dir(voyageai)}")
    
    # Try to create a client
    if hasattr(voyageai, 'get_client'):
        client = voyageai.get_client(api_key=api_key)
        print("Successfully created client using get_client")
    elif hasattr(voyageai, 'Client'):
        client = voyageai.Client(api_key=api_key)
        print("Successfully created client using Client class")
    else:
        print("Could not find a way to create a client, available attributes:")
        print(dir(voyageai))
        
except Exception as e:
    print(f"Error: {e}")
