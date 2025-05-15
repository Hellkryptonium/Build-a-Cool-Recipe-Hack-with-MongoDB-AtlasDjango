import os
import pymongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test the connection to MongoDB Atlas"""
    print("Testing MongoDB Atlas connection...")
    
    # Get the connection string from .env
    mongodb_uri = os.environ.get('MONGODB_URI')
    
    if not mongodb_uri:
        print("Error: MongoDB URI not found in environment variables.")
        print("Please make sure you have set the MONGODB_URI in your .env file.")
        return
    
    try:
        # Create a MongoDB client with SSL options
        client = pymongo.MongoClient(
            mongodb_uri,
            ssl=True,
            ssl_cert_reqs=pymongo.ssl_support.CERT_NONE,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            retryWrites=True,
            w='majority'
        )
        
        # Ping the database to verify the connection
        client.admin.command('ping')
        
        # Get database name from URI
        db_name = mongodb_uri.split('/')[-1].split('?')[0] or 'recipe_db'
        
        print("Successfully connected to MongoDB Atlas!")
        print(f"Database name: {db_name}")
        
        # List collections in the database
        db = client[db_name]
        collections = db.list_collection_names()
        
        if collections:
            print(f"Collections in the database: {', '.join(collections)}")
        else:
            print("No collections found in the database.")
        
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        print("Please check your connection string and make sure your IP is allowed in MongoDB Atlas.")

if __name__ == "__main__":
    test_mongodb_connection()
