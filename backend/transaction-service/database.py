from pymongo import MongoClient, ASCENDING, DESCENDING
from config import Config

client = None
db = None

def init_db():
    """Initialize MongoDB connection"""
    global client, db
    try:
        client = MongoClient(Config.MONGO_URI)
        db = client[Config.MONGO_DB_NAME]
        
        # Create indexes for better query performance
        db.transactions.create_index([('user_id', ASCENDING)])
        db.transactions.create_index([('date', DESCENDING)])
        db.transactions.create_index([('category', ASCENDING)])
        db.transactions.create_index([('type', ASCENDING)])
        db.transactions.create_index([
            ('user_id', ASCENDING),
            ('date', DESCENDING)
        ])
        
        print(f"Connected to MongoDB: {Config.MONGO_DB_NAME}")
        return db
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

def get_db():
    """Get database instance"""
    return db

def close_db():
    """Close MongoDB connection"""
    if client:
        client.close()
        print("MongoDB connection closed")
