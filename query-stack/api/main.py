from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
client = MongoClient(f"mongodb://{MONGO_HOST}:27017/")
db = client["query_db"]
users = db["users"]

app = FastAPI()

@app.get("/users/{email}")
def get_user(email: str):
    user = users.find_one({"_id": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.pop("_id")  # MongoDB's internal ID
    return user
