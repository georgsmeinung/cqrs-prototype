# app/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreateCommand(BaseModel):
    name: str
    email: EmailStr
