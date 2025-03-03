# Smart Home Management System

## Overview
The Smart Home Management System is a web-based application designed to manage users, houses, rooms, and devices within a smart home setup. The system consists of a frontend web interface (`index.html`) and a backend API built using FastAPI (`main.py`). The data models are defined in `models.py`.

## Files Description

### 1. `index.html`
This file provides the frontend interface for managing the smart home system. It includes:
- A sidebar for navigation between Users, Houses, Rooms, and Devices.
- A dashboard layout for displaying and interacting with different entities.
- Forms for adding, updating, and deleting users, houses, rooms, and devices.
- JavaScript for making API requests to the backend.

### 2. `main.py`
This is the backend API implemented using FastAPI. It provides CRUD operations for managing:
- Users
- Houses
- Rooms
- Devices

It also includes:
- CORS middleware configuration.
- Static file serving for the frontend.
- API endpoints for handling user, house, room, and device data.

### 3. `models.py`
This file defines the data models using Pydantic. The models include:
- `User`: Contains user details such as name, username, phone, and email.
- `House`: Represents a house with optional metadata.
- `Room`: Represents a room within a house, including floor and size information.
- `Device`: Represents a smart device within a room, with additional metadata options.

## Installation and Setup

### Prerequisites
Ensure you have Python installed (version 3.8 or later). Install FastAPI and Uvicorn using:
```bash
pip install fastapi uvicorn
```

### Running the Application
1. Start the FastAPI backend:
```bash
uvicorn main:app --reload
```
2. Open `index.html` in a browser or serve it using a static file server.

## API Endpoints

### Users
- `POST /users` - Create a new user.
- `GET /users` - Get all users.
- `GET /users/{username}` - Get details of a specific user.
- `PUT /users/{username}` - Update user details.
- `DELETE /users/{username}` - Delete a user.

### Houses
- `POST /houses` - Create a new house.
- `GET /houses` - Get all houses.
- `GET /houses/{name}` - Get details of a specific house.
- `PUT /houses/{name}` - Update house details.
- `DELETE /houses/{name}` - Delete a house.

### Rooms
- `POST /rooms` - Create a new room.
- `GET /rooms` - Get all rooms.
- `GET /rooms/{name}` - Get details of a specific room.
- `PUT /rooms/{name}` - Update room details.
- `DELETE /rooms/{name}` - Delete a room.

### Devices
- `POST /devices` - Create a new device.
- `GET /devices` - Get all devices.
- `GET /devices/{name}` - Get details of a specific device.
- `PUT /devices/{name}` - Update device details.
- `DELETE /devices/{name}` - Delete a device.

## Contributing
To contribute to this project, fork the repository, create a feature branch, and submit a pull request.

## License
This project is open-source and available under the MIT License.
