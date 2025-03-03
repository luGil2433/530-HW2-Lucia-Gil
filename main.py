from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse  # ✅ Import added
from pydantic import BaseModel
from typing import List, Optional
import re


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Static Files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

class User(BaseModel):
    username: str
    email: str
    phone: str
    full_name: str

class House(BaseModel):
    name: str
    address: str
    owner_username: str

class Room(BaseModel):
    name: str
    house_name: str
    type: str

class Device(BaseModel):
    name: str
    house_name: str
    room_name: str
    type: str
    status: str

users_db = []
houses_db = []
rooms_db = []
devices_db = []

# CRUD Endpoints for Users
@app.post("/users", response_model=User)
def create_user(user: User):
    users_db.append(user)
    return user

@app.get("/users", response_model=List[User])
def get_users():
    return users_db

@app.get("/users/{username}", response_model=User)
def get_user(username: str):
    for user in users_db:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{username}", response_model=User)
def update_user(username: str, updated_user: User):
    for index, user in enumerate(users_db):
        if user.username == username:
            users_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{username}")
def delete_user(username: str):
    global users_db
    users_db = [user for user in users_db if user.username != username]
    return {"message": "User deleted"}

# CRUD Endpoints for Houses
@app.post("/houses", response_model=House)
def create_house(house: House):
    # Check if owner_username exists
    if not any(user.username == house.owner_username for user in users_db):
        raise HTTPException(status_code=404, detail="Owner username not found")
    houses_db.append(house)
    return house

@app.get("/houses", response_model=List[House])
def get_houses():
    return houses_db

@app.get("/houses/{name}", response_model=House)
def get_house(name: str):
    for house in houses_db:
        if house.name == name:
            return house
    raise HTTPException(status_code=404, detail="House not found")

@app.put("/houses/{name}", response_model=House)
def update_house(name: str, updated_house: House):
    # Check if owner_username exists
    if not any(user.username == updated_house.owner_username for user in users_db):
        raise HTTPException(status_code=404, detail="Owner username not found")
    for index, house in enumerate(houses_db):
        if house.name == name:
            houses_db[index] = updated_house
            return updated_house
    raise HTTPException(status_code=404, detail="House not found")

@app.delete("/houses/{name}")
def delete_house(name: str):
    global houses_db
    houses_db = [house for house in houses_db if house.name != name]
    return {"message": "House deleted"}

# CRUD Endpoints for Rooms
@app.post("/rooms", response_model=Room)
def create_room(room: Room):
    # Check if house_name exists
    if not any(house.name == room.house_name for house in houses_db):
        raise HTTPException(status_code=404, detail="House not found")
    rooms_db.append(room)
    return room

@app.get("/rooms", response_model=List[Room])
def get_rooms():
    return rooms_db

@app.get("/rooms/{name}", response_model=Room)
def get_room(name: str):
    for room in rooms_db:
        if room.name == name:
            return room
    raise HTTPException(status_code=404, detail="Room not found")

@app.put("/rooms/{name}", response_model=Room)
def update_room(name: str, updated_room: Room):
    # Check if house_name exists
    if not any(house.name == updated_room.house_name for house in houses_db):
        raise HTTPException(status_code=404, detail="House not found")
    for index, room in enumerate(rooms_db):
        if room.name == name:
            rooms_db[index] = updated_room
            return updated_room
    raise HTTPException(status_code=404, detail="Room not found")

@app.delete("/rooms/{name}")
def delete_room(name: str):
    global rooms_db
    rooms_db = [room for room in rooms_db if room.name != name]
    return {"message": "Room deleted"}

# CRUD Endpoints for Devices
@app.post("/devices", response_model=Device)
def create_device(device: Device):
    # Check if house_name exists
    if not any(house.name == device.house_name for house in houses_db):
        raise HTTPException(status_code=404, detail="House not found")
    # Check if room_name exists under the same house
    if not any(room.name == device.room_name and room.house_name == device.house_name for room in rooms_db):
        raise HTTPException(status_code=404, detail="Room not found in the specified house")
    devices_db.append(device)
    return device

@app.get("/devices", response_model=List[Device])
def get_devices():
    return devices_db

@app.get("/devices/{name}", response_model=Device)
def get_device(name: str):
    for device in devices_db:
        if device.name == name:
            return device
    raise HTTPException(status_code=404, detail="Device not found")

@app.put("/devices/{name}", response_model=Device)
def update_device(name: str, updated_device: Device):
    # Check if house_name exists
    if not any(house.name == updated_device.house_name for house in houses_db):
        raise HTTPException(status_code=404, detail="House not found")
    # Check if room_name exists under the same house
    if not any(room.name == updated_device.room_name and room.house_name == updated_device.house_name for room in rooms_db):
        raise HTTPException(status_code=404, detail="Room not found in the specified house")
    for index, device in enumerate(devices_db):
        if device.name == name:
            devices_db[index] = updated_device
            return updated_device
    raise HTTPException(status_code=404, detail="Device not found")

@app.delete("/devices/{name}")
def delete_device(name: str):
    global devices_db
    devices_db = [device for device in devices_db if device.name != name]
    return {"message": "Device deleted"}

# Serve the HTML file
@app.get("/", response_class=HTMLResponse)
def get_html():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)