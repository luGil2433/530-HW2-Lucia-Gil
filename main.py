from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
import re
from pydantic import BaseModel

# Models
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

app = FastAPI()

# Enable CORS
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

@app.get("/users", response_model=List[User])
def get_users():
    return users_db

# House Endpoints
@app.post("/houses", response_model=House)
def create_house(house: House):
    # Check if owner exists
    if not any(user.username == house.owner_username for user in users_db):
        raise HTTPException(status_code=400, detail="Owner username does not exist")
    houses_db.append(house)
    return house

@app.get("/houses", response_model=List[House])
def get_houses():
    return houses_db

# Room Endpoints
@app.post("/rooms", response_model=Room)
def create_room(room: Room):
    # Check if house exists
    if not any(house.name == room.house_name for house in houses_db):
        raise HTTPException(status_code=400, detail="House does not exist")
    rooms_db.append(room)
    return room

@app.get("/rooms", response_model=List[Room])
def get_rooms():
    return rooms_db

# Device Endpoints
@app.post("/devices", response_model=Device)
def create_device(device: Device):
    # Check if house exists
    if not any(house.name == device.house_name for house in houses_db):
        raise HTTPException(status_code=400, detail="House does not exist")
    # Check if room exists in that house
    if not any(room.name == device.room_name and room.house_name == device.house_name for room in rooms_db):
        raise HTTPException(status_code=400, detail="Room does not exist in that house")
    devices_db.append(device)
    return device

@app.get("/devices", response_model=List[Device])
def get_devices():
    return devices_db

# Serve the HTML file
@app.get("/", response_class=HTMLResponse)
def get_html():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Home Management System</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #6b7280;
            --bg-color: #f9fafb;
            --card-bg: #ffffff;
            --text-color: #1f2937;
            --error: #ef4444;
            --success: #10b981;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1, h2, h3 {
            margin-bottom: 1rem;
            color: var(--primary-dark);
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        
        .sidebar {
            background-color: var(--card-bg);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .sidebar ul {
            list-style: none;
        }
        
        .sidebar li {
            margin-bottom: 10px;
        }
        
        .sidebar button {
            background: none;
            border: none;
            color: var(--primary);
            cursor: pointer;
            text-align: left;
            width: 100%;
            padding: 8px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        
        .sidebar button:hover {
            background-color: rgba(37, 99, 235, 0.1);
        }
        
        .sidebar button.active {
            background-color: var(--primary);
            color: white;
        }
        
        .content {
            background-color: var(--card-bg);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid var(--secondary);
            border-radius: 4px;
            font-size: 16px;
        }
        
        button {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.2s;
        }
        
        button:hover {
            background-color: var(--primary-dark);
        }
        
        .error-message {
            color: var(--error);
            margin-top: 10px;
        }
        
        .success-message {
            color: var(--success);
            margin-top: 10px;
        }
        
        .card {
            background-color: var(--card-bg);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .card h3 {
            margin-bottom: 0.5rem;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 5px;
        }
        
        .entity-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .back-button {
            background-color: var(--secondary);
            margin-bottom: 15px;
        }
        
        .action-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Home Management System</h1>
        
        <div class="dashboard">
            <div class="sidebar">
                <h2>Navigation</h2>
                <ul>
                    <li><button id="nav-users" class="active">Users</button></li>
                    <li><button id="nav-houses">Houses</button></li>
                    <li><button id="nav-rooms">Rooms</button></li>
                    <li><button id="nav-devices">Devices</button></li>
                </ul>
            </div>
            
            <div class="content" id="content">
                <!-- Content will be loaded dynamically -->
            </div>
        </div>
    </div>

    <script>
        // Base URL for API - now we can use relative URLs since we're on the same origin
        const API_BASE_URL = '';
        
        // In-memory cache for entities
        const cache = {
            users: [],
            houses: [],
            rooms: [],
            devices: []
        };
        
        // Current active section
        let activeSection = 'users';
        
        // DOM Elements
        const contentEl = document.getElementById('content');
        const navButtons = {
            users: document.getElementById('nav-users'),
            houses: document.getElementById('nav-houses'),
            rooms: document.getElementById('nav-rooms'),
            devices: document.getElementById('nav-devices')
        };
        
        // Add event listeners to navigation buttons
        Object.keys(navButtons).forEach(section => {
            navButtons[section].addEventListener('click', () => {
                setActiveSection(section);
            });
        });
        
        // Set active section and update UI
        function setActiveSection(section) {
            activeSection = section;
            
            // Update active button
            Object.values(navButtons).forEach(btn => btn.classList.remove('active'));
            navButtons[section].classList.add('active');
            
            // Load content for the section
            loadSectionContent(section);
        }
        
        // Load content for a section
        function loadSectionContent(section) {
            switch(section) {
                case 'users':
                    showUserSection();
                    break;
                case 'houses':
                    showHouseSection();
                    break;
                case 'rooms':
                    showRoomSection();
                    break;
                case 'devices':
                    showDeviceSection();
                    break;
            }
        }
        
        // Users Section
        function showUserSection() {
            const html = `
                <h2>Users</h2>
                <button id="add-user-btn">Add New User</button>
                <div id="user-form-container" style="display: none; margin-top: 20px;">
                    <div class="card">
                        <h3>Add User</h3>
                        <form id="user-form">
                            <div class="form-group">
                                <label for="username">Username</label>
                                <input type="text" id="username" required>
                            </div>
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" id="email" required>
                            </div>
                            <div class="form-group">
                                <label for="phone">Phone</label>
                                <input type="text" id="phone" required>
                            </div>
                            <div class="form-group">
                                <label for="full_name">Full Name</label>
                                <input type="text" id="full_name" required>
                            </div>
                            <button type="submit">Save User</button>
                        </form>
                        <div id="user-form-message"></div>
                    </div>
                </div>
                <div id="user-list" class="entity-list">
                    <!-- Users will be loaded here -->
                    <p>Loading users...</p>
                </div>
            `;
            
            contentEl.innerHTML = html;
            
            // Add event listeners
            document.getElementById('add-user-btn').addEventListener('click', () => {
                document.getElementById('user-form-container').style.display = 'block';
            });
            
            document.getElementById('user-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = {
                    username: document.getElementById('username').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    full_name: document.getElementById('full_name').value
                };
                
                try {
                    const response = await fetch(`${API_BASE_URL}/users`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to create user');
                    }
                    
                    const data = await response.json();
                    document.getElementById('user-form-message').innerHTML = `
                        <div class="success-message">User created successfully!</div>
                    `;
                    document.getElementById('user-form').reset();
                    loadUsers();
                } catch (error) {
                    document.getElementById('user-form-message').innerHTML = `
                        <div class="error-message">${error.message}</div>
                    `;
                }
            });
            
            // Load users
            loadUsers();
        }
        
        async function loadUsers() {
            const userListEl = document.getElementById('user-list');
            userListEl.innerHTML = '<p>Loading users...</p>';
            
            try {
                const response = await fetch(`${API_BASE_URL}/users`);
                
                if (!response.ok) {
                    throw new Error('Failed to load users');
                }
                
                const users = await response.json();
                
                if (users.length === 0) {
                    userListEl.innerHTML = '<p>No users available yet. Add some users to see them here.</p>';
                } else {
                    userListEl.innerHTML = users.map(user => `
                        <div class="card">
                            <h3>${user.username}</h3>
                            <p><strong>Full Name:</strong> ${user.full_name}</p>
                            <p><strong>Email:</strong> ${user.email}</p>
                            <p><strong>Phone:</strong> ${user.phone}</p>
                        </div>
                    `).join('');
                }
            } catch (error) {
                userListEl.innerHTML = `<div class="error-message">Error loading users: ${error.message}</div>`;
            }
        }
        
        // Houses Section
        function showHouseSection() {
            const html = `
                <h2>Houses</h2>
                <button id="add-house-btn">Add New House</button>
                <div id="house-form-container" style="display: none; margin-top: 20px;">
                    <div class="card">
                        <h3>Add House</h3>
                        <form id="house-form">
                            <div class="form-group">
                                <label for="house-name">Name</label>
                                <input type="text" id="house-name" required>
                            </div>
                            <div class="form-group">
                                <label for="house-address">Address</label>
                                <input type="text" id="house-address" required>
                            </div>
                            <div class="form-group">
                                <label for="house-owner">Owner Username</label>
                                <input type="text" id="house-owner" required>
                            </div>
                            <button type="submit">Save House</button>
                        </form>
                        <div id="house-form-message"></div>
                    </div>
                </div>
                <div id="house-list" class="entity-list">
                    <!-- Houses will be loaded here -->
                    <p>Loading houses...</p>
                </div>
            `;
            
            contentEl.innerHTML = html;
            
            // Add event listeners
            document.getElementById('add-house-btn').addEventListener('click', () => {
                document.getElementById('house-form-container').style.display = 'block';
            });
            
            document.getElementById('house-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = {
                    name: document.getElementById('house-name').value,
                    address: document.getElementById('house-address').value,
                    owner_username: document.getElementById('house-owner').value
                };
                
                try {
                    const response = await fetch(`${API_BASE_URL}/houses`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to create house');
                    }
                    
                    const data = await response.json();
                    document.getElementById('house-form-message').innerHTML = `
                        <div class="success-message">House created successfully!</div>
                    `;
                    document.getElementById('house-form').reset();
                    loadHouses();
                } catch (error) {
                    document.getElementById('house-form-message').innerHTML = `
                        <div class="error-message">${error.message}</div>
                    `;
                }
            });
            
            // Load houses
            loadHouses();
        }
        
        async function loadHouses() {
            const houseListEl = document.getElementById('house-list');
            houseListEl.innerHTML = '<p>Loading houses...</p>';
            
            try {
                const response = await fetch(`${API_BASE_URL}/houses`);
                
                if (!response.ok) {
                    throw new Error('Failed to load houses');
                }
                
                const houses = await response.json();
                
                if (houses.length === 0) {
                    houseListEl.innerHTML = '<p>No houses available yet. Add some houses to see them here.</p>';
                } else {
                    houseListEl.innerHTML = houses.map(house => `
                        <div class="card">
                            <h3>${house.name}</h3>
                            <p><strong>Address:</strong> ${house.address}</p>
                            <p><strong>Owner:</strong> ${house.owner_username}</p>
                        </div>
                    `).join('');
                }
            } catch (error) {
                houseListEl.innerHTML = `<div class="error-message">Error loading houses: ${error.message}</div>`;
            }
        }
        
        // Rooms Section
        function showRoomSection() {
            const html = `
                <h2>Rooms</h2>
                <button id="add-room-btn">Add New Room</button>
                <div id="room-form-container" style="display: none; margin-top: 20px;">
                    <div class="card">
                        <h3>Add Room</h3>
                        <form id="room-form">
                            <div class="form-group">
                                <label for="room-name">Name</label>
                                <input type="text" id="room-name" required>
                            </div>
                            <div class="form-group">
                                <label for="room-house">House Name</label>
                                <input type="text" id="room-house" required>
                            </div>
                            <div class="form-group">
                                <label for="room-type">Type</label>
                                <select id="room-type" required>
                                    <option value="Living Room">Living Room</option>
                                    <option value="Bedroom">Bedroom</option>
                                    <option value="Kitchen">Kitchen</option>
                                    <option value="Bathroom">Bathroom</option>
                                    <option value="Office">Office</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <button type="submit">Save Room</button>
                        </form>
                        <div id="room-form-message"></div>
                    </div>
                </div>
                <div id="room-list" class="entity-list">
                    <!-- Rooms will be loaded here -->
                    <p>Loading rooms...</p>
                </div>
            `;
            
            contentEl.innerHTML = html;
            
            // Add event listeners
            document.getElementById('add-room-btn').addEventListener('click', () => {
                document.getElementById('room-form-container').style.display = 'block';
            });
            
            document.getElementById('room-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = {
                    name: document.getElementById('room-name').value,
                    house_name: document.getElementById('room-house').value,
                    type: document.getElementById('room-type').value
                };
                
                try {
                    const response = await fetch(`${API_BASE_URL}/rooms`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to create room');
                    }
                    
                    const data = await response.json();
                    document.getElementById('room-form-message').innerHTML = `
                        <div class="success-message">Room created successfully!</div>
                    `;
                    document.getElementById('room-form').reset();
                    loadRooms();
                } catch (error) {
                    document.getElementById('room-form-message').innerHTML = `
                        <div class="error-message">${error.message}</div>
                    `;
                }
            });
            
            // Load rooms
            loadRooms();
        }
        
        async function loadRooms() {
            const roomListEl = document.getElementById('room-list');
            roomListEl.innerHTML = '<p>Loading rooms...</p>';
            
            try {
                const response = await fetch(`${API_BASE_URL}/rooms`);
                
                if (!response.ok) {
                    throw new Error('Failed to load rooms');
                }
                
                const rooms = await response.json();
                
                if (rooms.length === 0) {
                    roomListEl.innerHTML = '<p>No rooms available yet. Add some rooms to see them here.</p>';
                } else {
                    roomListEl.innerHTML = rooms.map(room => `
                        <div class="card">
                            <h3>${room.name}</h3>
                            <p><strong>House:</strong> ${room.house_name}</p>
                            <p><strong>Type:</strong> ${room.type}</p>
                        </div>
                    `).join('');
                }
            } catch (error) {
                roomListEl.innerHTML = `<div class="error-message">Error loading rooms: ${error.message}</div>`;
            }
        }
        
        // Devices Section
        function showDeviceSection() {
            const html = `
                <h2>Devices</h2>
                <button id="add-device-btn">Add New Device</button>
                <div id="device-form-container" style="display: none; margin-top: 20px;">
                    <div class="card">
                        <h3>Add Device</h3>
                        <form id="device-form">
                            <div class="form-group">
                                <label for="device-name">Name</label>
                                <input type="text" id="device-name" required>
                            </div>
                            <div class="form-group">
                                <label for="device-house">House Name</label>
                                <input type="text" id="device-house" required>
                            </div>
                            <div class="form-group">
                                <label for="device-room">Room Name</label>
                                <input type="text" id="device-room" required>
                            </div>
                            <div class="form-group">
                                <label for="device-type">Type</label>
                                <select id="device-type" required>
                                    <option value="Light">Light</option>
                                    <option value="Thermostat">Thermostat</option>
                                    <option value="Lock">Lock</option>
                                    <option value="Camera">Camera</option>
                                    <option value="Speaker">Speaker</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="device-status">Status</label>
                                <select id="device-status" required>
                                    <option value="on">On</option>
                                    <option value="off">Off</option>
                                </select>
                            </div>
                            <button type="submit">Save Device</button>
                        </form>
                        <div id="device-form-message"></div>
                    </div>
                </div>
                <div id="device-list" class="entity-list">
                    <!-- Devices will be loaded here -->
                    <p>Loading devices...</p>
                </div>
            `;
            
            contentEl.innerHTML = html;
            
            // Add event listeners
            document.getElementById('add-device-btn').addEventListener('click', () => {
                document.getElementById('device-form-container').style.display = 'block';
            });
            
            document.getElementById('device-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = {
                    name: document.getElementById('device-name').value,
                    house_name: document.getElementById('device-house').value,
                    room_name: document.getElementById('device-room').value,
                    type: document.getElementById('device-type').value,
                    status: document.getElementById('device-status').value
                };
                
                try {
                    const response = await fetch(`${API_BASE_URL}/devices`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to create device');
                    }
                    
                    const data = await response.json();
                    document.getElementById('device-form-message').innerHTML = `
                        <div class="success-message">Device created successfully!</div>
                    `;
                    document.getElementById('device-form').reset();
                    loadDevices();
                } catch (error) {
                    document.getElementById('device-form-message').innerHTML = `
                        <div class="error-message">${error.message}</div>
                    `;
                }
            });
            
            // Load devices
            loadDevices();
        }
        
        async function loadDevices() {
            const deviceListEl = document.getElementById('device-list');
            deviceListEl.innerHTML = '<p>Loading devices...</p>';
            
            try {
                const response = await fetch(`${API_BASE_URL}/devices`);
                
                if (!response.ok) {
                    throw new Error('Failed to load devices');
                }
                
                const devices = await response.json();
                
                if (devices.length === 0) {
                    deviceListEl.innerHTML = '<p>No devices available yet. Add some devices to see them here.</p>';
                } else {
                    deviceListEl.innerHTML = devices.map(device => `
                        <div class="card">
                            <h3>${device.name}</h3>
                            <p><strong>House:</strong> ${device.house_name}</p>
                            <p><strong>Room:</strong> ${device.room_name}</p>
                            <p><strong>Type:</strong> ${device.type}</p>
                            <p><strong>Status:</strong> <span style="color: ${device.status === 'on' ? 'var(--success)' : 'var(--error)'}">
                                ${device.status.toUpperCase()}</span></p>
                        </div>
                    `).join('');
                }
            } catch (error) {
                deviceListEl.innerHTML = `<div class="error-message">Error loading devices: ${error.message}</div>`;
            }
        }
        
        // Initialize the app
        setActiveSection('users');
    </script>
</body>
</html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)