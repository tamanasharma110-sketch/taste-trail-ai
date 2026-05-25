from pymongo import MongoClient


class MongoDBClient:

    def __init__(self):
        self.client = MongoClient("mongodb+srv://admin:Password123@cluster0.5wwy4ir.mongodb.net/?appName=Cluster0")
        self.db = self.client["tastetrail"]

    def get_all_restaurants(self):
        return list(self.db["restaurants"].find({}))