from pymongo import MongoClient
import datetime

class MongoHandler:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client['farmer_assistant']
        self.collection = self.db['crop_insights']

    def save_crop_analysis(self, crop, mandi_data, trend, advice):
        """Saves prediction results to MongoDB."""
        data = {
            "crop": crop,
            "last_updated": datetime.datetime.now(),
            "best_mandi": mandi_data, # dictionary
            "demand_trend": trend,
            "storage_advice": advice
        }
        # Update if crop exists, otherwise insert (Upsert)
        self.collection.update_one({"crop": crop}, {"$set": data}, upsert=True)

    def fetch_crop_insight(self, crop):
        """Retrieves data for the AI Assistant."""
        return self.collection.find_one({"crop": crop})