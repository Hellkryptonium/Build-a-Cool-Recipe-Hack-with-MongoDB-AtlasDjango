import os
import json
import requests
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get Gemini API key
gemini_api_key = os.environ.get('GEMINI_API_KEY')

def generate_recipe_embedding(text_to_embed):
    """Generates an embedding for the given text using Google Gemini."""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            return [0.0] * 768 # Return a default placeholder embedding

        model_name = "embedding-001" # Correct model for embeddings
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:embedContent?key={api_key}"

        payload = {"content": {"parts": [{"text": text_to_embed}]}}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        embedding = response.json().get("embedding", {}).get("values")
        
        if not embedding:
            logger.error(f"Failed to extract embedding from Gemini API response for text: {text_to_embed[:50]}...")
            return [0.0] * 768 # Default embedding dimension for embedding-001 is 768

        logger.info(f"Successfully generated embedding for: {text_to_embed[:50]}...")
        return embedding

    except requests.exceptions.RequestException as e:
        logger.error(f"Error generating embedding with Gemini (RequestException): {e} for text: {text_to_embed[:50]}...")
        if e.response is not None:
            logger.error(f"Gemini API Response Text: {e.response.text}")
        return [0.0] * 768 # Placeholder for error
    except Exception as e:
        logger.error(f"Unexpected error in generate_recipe_embedding: {e} for text: {text_to_embed[:50]}...")
        return [0.0] * 768 # Placeholder for error

def get_recipe_suggestions(recipe):
    """
    Get recipe suggestions using Google Gemini based on the input recipe
    
    Args:
        recipe: Recipe object
        
    Returns:
        List of suggestion dictionaries
    """
    try:
        # Create a prompt for Gemini
        prompt = f"""
        I have a recipe with the following details:
        
        Title: {recipe.title}
        Category: {recipe.category}
        Ingredients: 
        {recipe.ingredients}
        
        Based on these ingredients and the recipe type, please suggest 3 related recipes that 
        would be interesting to try. For each suggestion, include:
        1. A creative title
        2. A short list of main ingredients
        3. A brief description
        
        Format your response as JSON with this structure:
        [
            {{"title": "Recipe Title", "ingredients": ["ingredient1", "ingredient2"], "description": "Recipe description"}},
            ...
        ]
        
        Only provide the JSON array, no additional text.
        """
        
        # Build request for Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        # Extract and parse the JSON response
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            content = response_json['candidates'][0]['content']
            if 'parts' in content and len(content['parts']) > 0:
                response_text = content['parts'][0]['text']
                # Clean the response text (in case there's extra text before or after the JSON)
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_text = response_text[start_idx:end_idx]
                    suggestions = json.loads(json_text)
                    return suggestions
        
        # If we couldn't get a proper response, return an empty list
        print("Failed to parse Gemini response or no candidates returned")
        return []
    except Exception as e:
        print(f"Error getting recipe suggestions: {e}")
        return []
