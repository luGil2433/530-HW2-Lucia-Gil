from pydantic import BaseModel
from typing import Optional, Dict

class User(BaseModel):
    name: str
    username: str
    phone: str
    email: str

class House(BaseModel):
    name: str
    metadata: Optional[Dict] = {}

class Room(BaseModel):
    house_name: str
    name: str
    floor: int
    size: str
    metadata: Optional[Dict] = {}

class Device(BaseModel):
    house_name: str
    room_name: str
    type: str
    name: str
    metadata: Optional[Dict] = {}
