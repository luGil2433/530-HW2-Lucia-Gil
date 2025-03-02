from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import re
from models import User, House, Room, Device

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database"
users_db = []
houses_db = []
rooms_db = []
devices_db = []

# User Endpoints
@app.post("/users", response_model=User)
def create_user(user: User):
    if not re.match(r"^\+?\d+$", user.phone) or not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(status_code=400, detail="Invalid phone number or email format")
    users_db.append(user)
    return user

@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    for user in users_db:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# House Endpoints
@app.post("/houses", response_model=House)
def create_house(house: House):
    houses_db.append(house)
    return house

@app.get("/houses/{house_name}", response_model=House)
def read_house(house_name: str):
    for house in houses_db:
        if house.name == house_name:
            return house
    raise HTTPException(status_code=404, detail="House not found")

# Room Endpoints
@app.post("/rooms", response_model=Room)
def create_room(room: Room):
    rooms_db.append(room)
    return room

@app.get("/rooms/{house_name}/{room_name}", response_model=Room)
def read_room(house_name: str, room_name: str):
    for room in rooms_db:
        if room.house_name == house_name and room.name == room_name:
            return room
    raise HTTPException(status_code=404, detail="Room not found")

# Device Endpoints
@app.post("/devices", response_model=Device)
def create_device(device: Device):
    devices_db.append(device)
    return device

@app.get("/devices/{house_name}/{room_name}/{device_name}", response_model=Device)
def read_device(house_name: str, room_name: str, device_name: str):
    for device in devices_db:
        if device.house_name == house_name and device.room_name == room_name and device.name == device_name:
            return device
    raise HTTPException(status_code=404, detail="Device not found")

