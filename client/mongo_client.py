from pymongo import MongoClient
from core.settings import settings
client = MongoClient("mongodb://localhost:27017")
db = client[settings.MONGO_DB_NAME]