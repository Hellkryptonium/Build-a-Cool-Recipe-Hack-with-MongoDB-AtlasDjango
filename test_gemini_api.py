import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the connection to Google Gemini API"""
    print("Testing Google Gemini API connection...")
    
    # Get the API key from .env
    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    
    if not gemini_api_key:
        print("Error: Google Gemini API key not found in environment variables.")
        print("Please make sure you have set the GEMINI_API_KEY in your .env file.")
        return
    
    try:
        # Prepare test request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": "Give me a simple recipe idea using chicken and pasta."}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }
        
        # Make the API request
        print("Sending request to Gemini API...")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            
            if 'candidates' in response_json and len(response_json['candidates']) > 0:
                content = response_json['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    text = content['parts'][0]['text']
                    print("\nSuccessfully received response from Gemini API!")
                    print("\nSample response (first 300 chars):")
                    print("-" * 50)
                    print(text[:300] + "...")
                    print("-" * 50)
                    return
        
        # If we get here, something went wrong
        print(f"Error: Failed to get a proper response from Gemini API.")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error testing Gemini API: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    test_gemini_api()
