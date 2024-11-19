from pymongo import MongoClient
import os


mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = int(os.getenv("MONGO_PORT", "27018"))
mongo_user = os.getenv("MONGO_USER", "scoutlens_admin")
mongo_password = os.getenv("MONGO_PASSWORD", "password")
mongo_db = os.getenv("MONGO_DB", "scoutlens")
mongo_collection = os.getenv("MONGO_COLLECTION", "players_reports")
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"


class MongoService:
    # MongoDB setup
    def __init__(self):
        # Connect to MongoDB
        print(mongo_uri)
        self.client = MongoClient(mongo_uri)
        db = self.client[mongo_db]
        self.collection = db[mongo_collection]

    def save_report_to_db(self, report_data):
        self.collection.insert_one(report_data)

    def get_report_by_rank(self, rank):
        return self.collection.find_one({"rank": rank})


mongo_service = MongoService()
