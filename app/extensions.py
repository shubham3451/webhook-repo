from pymongo import MongoClient, ASCENDING
from app.config import MONGO_URI, DB_NAME, COLLECTION_NAME


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
collection.create_index([("timestamp", ASCENDING)])
