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
    houses_db.append(house)
    return house

@app.get("/houses", response_model=List[House])
def get_houses():
    return houses_db

@app.put("/houses/{name}", response_model=House)
def update_house(name: str, updated_house: House):
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

# Serve the HTML file
@app.get("/", response_class=HTMLResponse)
def get_html():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
