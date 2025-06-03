from decouple import config

# Load environment variables from .env file


# GitHub webhook secret
GITHUB_SECRET = config("SECRET_TOKEN")

# MongoDB connection info
MONGO_URI = config("MONGO_URI")
DB_NAME = config("DB_NAME")
COLLECTION_NAME = config("COLLECTION_NAME")

