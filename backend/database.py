from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from typing import Dict, Any
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "password")
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
DB_NAME = os.getenv("MONGO_INITDB_DATABASE", "translation_db")
COLLECTION_NAME = "translation_logs"

# Construct MongoDB URI
MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{DB_NAME}?authSource=admin"

# Log MongoDB connection details (don't log credentials in production)
logger.info(f"Connecting to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
logger.info(f"Using database: {DB_NAME}")

# Initialize MongoDB client
try:
    client = MongoClient(
        MONGODB_URI,
        server_api=ServerApi('1'),
        serverSelectionTimeoutMS=5000  # 5 second timeout
    )
    
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB!")
    
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Create an index on timestamp for faster queries
    collection.create_index("timestamp")
    
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

def log_translation(input_text: str, output_text: str, metadata: Dict[str, Any] = None) -> str:
    """
    Log a translation to the database.
    
    Args:
        input_text: The original text that was translated
        output_text: The translated text
        metadata: Additional metadata to store (e.g., model used, timings)
    
    Returns:
        str: The ID of the inserted document
    """
    if metadata is None:
        metadata = {}
    
    document = {
        "input_text": input_text,
        "output_text": output_text,
        "timestamp": datetime.utcnow(),
        **metadata
    }
    
    result = collection.insert_one(document)
    return str(result.inserted_id)

def get_recent_translations(limit: int = 10) -> list:
    """
    Retrieve recent translations from the database.
    
    Args:
        limit: Maximum number of translations to return
        
    Returns:
        list: List of recent translation documents
    """
    cursor = collection.find().sort("timestamp", -1).limit(limit)
    return list(cursor)
