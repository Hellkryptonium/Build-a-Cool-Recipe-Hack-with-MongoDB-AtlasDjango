import os
import sys
import pymongo
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection string
mongodb_uri = os.environ.get("MONGODB_URI")

def test_mongodb_recipe_operations():
    """Test basic MongoDB operations directly for recipes"""
    print("Testing direct MongoDB connectivity...")
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongodb_uri)
        db = client.get_database()  # This will use the database from the connection string
        
        # Print database and collection info
        print(f"Connected to database: {db.name}")
        print(f"Collections: {db.list_collection_names()}")
        
        # Check if recipes_recipe collection exists and count documents
        if 'recipes_recipe' in db.list_collection_names():
            count = db.recipes_recipe.count_documents({})
            print(f"recipes_recipe collection exists with {count} documents")
            
            # Show sample recipe(s)
            sample = list(db.recipes_recipe.find().limit(2))
            print(f"Sample recipes: {sample}")
        else:
            print("recipes_recipe collection does not exist yet")
        
        # Test creating a recipe directly
        test_recipe = {
            "_id": ObjectId(),
            "title": "Test Direct MongoDB Recipe",
            "ingredients": "Test ingredients",
            "instructions": "Test instructions",
            "cooking_time": 30,
            "servings": 4,
            "category": "Test"
        }
        
        result = db.recipes_recipe.insert_one(test_recipe)
        print(f"Inserted recipe with id: {result.inserted_id}")
        
        # Verify it was inserted
        found = db.recipes_recipe.find_one({"_id": result.inserted_id})
        print(f"Retrieved recipe: {found}")
        
        # Clean up
        db.recipes_recipe.delete_one({"_id": result.inserted_id})
        print("Test recipe deleted")
        
        client.close()
        print("MongoDB connection closed")
        return True
    except Exception as e:
        print(f"MongoDB test error: {e}")
        return False

if __name__ == "__main__":
    success = test_mongodb_recipe_operations()
    sys.exit(0 if success else 1)
