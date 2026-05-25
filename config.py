import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("mongodb+srv://admin:Password123@cluster0.5wwy4ir.mongodb.net/?appName=Cluster0")
GEMINI_API_KEY = os.getenv("AIzaSyAn_VD6rQX2gqCA8Qz9D7p-_S8S36KL0gg")