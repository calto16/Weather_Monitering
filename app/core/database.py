import pymongo
from app.core.config import MONGODB_URL, DB_NAME

client = pymongo.MongoClient(MONGODB_URL)
db = client[DB_NAME]

weather_collection = db["weather_data"]
threshold_collection = db["alert_thresholds"]
summary_collection = db["weather_summaries"]