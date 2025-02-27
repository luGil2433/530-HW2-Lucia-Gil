# Smart Home API Test Suite

A comprehensive test suite for the Smart Home API system that tests user management, house configuration, room setup, and device control functionality.

## Overview

This test suite provides coverage for four main API classes:
- UserAPI: Manages user accounts and profiles
- HouseAPI: Handles house creation and configuration
- RoomAPI: Manages rooms within houses
- DeviceAPI: Controls smart devices within rooms


## Project Structure

```
smart-home-api/
├── homeAPI.py         # Main API implementation
├── test_home_api.py   # Test suite
├── main.py             # Text input by user
└── README.md          # This file
```

## API Usage Examples

### Creating a User
```python
user_api = UserAPI()
user = user_api.create_user(
    "John Doe",
    "johndoe",
    "+1234567890",
    "john@example.com"
)
```

### Creating a House
```python
house_api = HouseAPI()
house = house_api.create_house(
    "My Smart Home",
    address="123 Main St",
    gps_location="40.7128,-74.0060"
)
```

### Adding a Room
```python
room_api = RoomAPI()
room = room_api.create_room(
    "My Smart Home",
    "Living Room",
    1,
    "Large",
    color="Blue"
)
```

### Adding a Device
```python
device_api = DeviceAPI()
device = device_api.create_device(
    "My Smart Home",
    "Living Room",
    "Light",
    "Ceiling Light",
    brightness=80
)
```
