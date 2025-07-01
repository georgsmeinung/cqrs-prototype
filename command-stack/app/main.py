# app/main.py
from fastapi import FastAPI
from app.schemas import UserCreateCommand
from app.producer import publish_user_created
from uuid import uuid4
from datetime import datetime

app = FastAPI()

@app.post("/users")
def create_user(user: UserCreateCommand):
    event = {
        "event_id": str(uuid4()),
        "type": "user.created",
        "timestamp": datetime.utcnow().isoformat(),
        "payload": user.dict()
    }
    publish_user_created(event)
    return {"status": "event_published", "event": event}
