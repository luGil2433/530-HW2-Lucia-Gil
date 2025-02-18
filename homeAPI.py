import re

class DeviceAPI:
    def create_device(self, house_name, room_name, device_type, device_name, **metadata):
        if not all([house_name, room_name, device_type, device_name]):
            raise ValueError("House name, room name, device type, and device name are required.")
        print(f"Creating device '{device_name}' of type '{device_type}' in room '{room_name}' of house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": room_name, "device": {"type": device_type, "name": device_name, "metadata": metadata}}
    
    def delete_device(self, house_name, room_name, device_name):
        if not all([house_name, room_name, device_name]):
            raise ValueError("House name, room name, and device name are required.")
        print(f"Deleting device '{device_name}' from room '{room_name}' in house '{house_name}'")
        return True
    
    def read_device(self, house_name, room_name, device_name):
        if not all([house_name, room_name, device_name]):
            raise ValueError("House name, room name, and device name are required.")
        print(f"Reading device '{device_name}' in room '{room_name}' of house '{house_name}'")
        return {"house": house_name, "room": room_name, "device": {"name": device_name, "data": {"temperature": 22, "humidity": 50}}}
    
    def update_device(self, house_name, room_name, device_name, **metadata):
        if not all([house_name, room_name, device_name]):
            raise ValueError("House name, room name, and device name are required.")
        print(f"Updating device '{device_name}' in room '{room_name}' of house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": room_name, "device": {"name": device_name, "updated_metadata": metadata}}


class HouseAPI:
    def create_house(self, house_name, **metadata):
        if not house_name:
            raise ValueError("House name is required.")
        print(f"Creating house '{house_name}' with metadata: {metadata}")
        return {"name": house_name, "metadata": metadata, "rooms": []}
    
    def delete_house(self, house_name):
        if not house_name:
            raise ValueError("House name is required.")
        print(f"Deleting house '{house_name}'")
        return True
    
    def read_house(self, house_name):
        if not house_name:
            raise ValueError("House name is required.")
        print(f"Reading house '{house_name}'")
        return {"name": house_name, "metadata": {}, "rooms": []}
    
    def update_house(self, house_name, **metadata):
        if not house_name:
            raise ValueError("House name is required.")
        print(f"Updating house '{house_name}' with metadata: {metadata}")
        return {"name": house_name, "updated_metadata": metadata}


class RoomAPI:
    def create_room(self, house_name, room_name, floor, size, **metadata):
        if not all([house_name, room_name]) or not isinstance(floor, int) or not isinstance(size, str):
            raise ValueError("House name, room name, floor (int), and size (str) are required.")
        print(f"Creating room '{room_name}' on floor '{floor}' in house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": {"name": room_name, "floor": floor, "size": size, "metadata": metadata, "devices": []}}
    
    def delete_room(self, house_name, room_name):
        if not all([house_name, room_name]):
            raise ValueError("House name and room name are required.")
        print(f"Deleting room '{room_name}' from house '{house_name}'")
        return True
    
    def read_room(self, house_name, room_name):
        if not all([house_name, room_name]):
            raise ValueError("House name and room name are required.")
        print(f"Reading room '{room_name}' in house '{house_name}'")
        return {"house": house_name, "room": {"name": room_name, "metadata": {}, "devices": []}}
    
    def update_room(self, house_name, room_name, **metadata):
        if not all([house_name, room_name]):
            raise ValueError("House name and room name are required.")
        print(f"Updating room '{room_name}' in house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": {"name": room_name, "updated_metadata": metadata}}


class UserAPI:
    def create_user(self, name, username, phone, email):
        if not all([name, username, phone, email]) or not re.match(r"^\+?\d+$", phone) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Valid name, username, phone number, and email are required.")
        print(f"Creating user '{username}' with name '{name}', phone '{phone}', and email '{email}'")
        return {"name": name, "username": username, "phone": phone, "email": email}
    
    def delete_user(self, username):
        if not username:
            raise ValueError("Username is required.")
        print(f"Deleting user '{username}'")
        return True
    
    def read_user(self, username):
        if not username:
            raise ValueError("Username is required.")
        print(f"Reading user '{username}'")
        return {"username": username, "name": "Example User", "phone": "0000000000", "email": "example@example.com"}
    
    def update_user(self, username, **attributes):
        if not username:
            raise ValueError("Username is required.")
        print(f"Updating user '{username}' with attributes: {attributes}")
        return {"username": username, "updated_attributes": attributes}
