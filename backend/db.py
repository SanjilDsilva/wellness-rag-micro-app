from pymongo import MongoClient
from datetime import datetime
import os

client = None
db = None
collection = None


def init_db():
    global client, db, collection

    mongodb_uri = os.getenv("MONGODB_URI")

    if not mongodb_uri:
        raise ValueError("MONGODB_URI not set in environment variables")

    client = MongoClient(mongodb_uri)
    db = client["wellness_rag"]
    collection = db["interactions"]


def log_interaction(
    query: str,
    is_unsafe: bool,
    retrieved_chunks: list,
    response: str
):
    if collection is None:
        return

    log = {
        "query": query,
        "isUnsafe": is_unsafe,
        "retrievedChunks": retrieved_chunks,
        "response": response,
        "timestamp": datetime.utcnow()
    }

    try:
        collection.insert_one(log)
    except Exception as e:
        print("MongoDB logging failed:", e)
