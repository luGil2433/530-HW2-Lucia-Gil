class DeviceAPI:
    def create_device(self, house_name, room_name, device_type, device_name, **metadata):
        print(f"Creating device '{device_name}' of type '{device_type}' in room '{room_name}' of house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": room_name, "device": {"type": device_type, "name": device_name, "metadata": metadata}}
    
    def delete_device(self, house_name, room_name, device_name):
        print(f"Deleting device '{device_name}' from room '{room_name}' in house '{house_name}'")
        return True
    
    def read_device(self, house_name, room_name, device_name):
        print(f"Reading device '{device_name}' in room '{room_name}' of house '{house_name}'")
        return {"house": house_name, "room": room_name, "device": {"name": device_name, "data": {"temperature": 22, "humidity": 50}}}
    
    def update_device(self, house_name, room_name, device_name, **metadata):
        print(f"Updating device '{device_name}' in room '{room_name}' of house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": room_name, "device": {"name": device_name, "updated_metadata": metadata}}


class HouseAPI:
    def create_house(self, house_name, **metadata):
        print(f"Creating house '{house_name}' with metadata: {metadata}")
        return {"name": house_name, "metadata": metadata, "rooms": []}
    
    def delete_house(self, house_name):
        print(f"Deleting house '{house_name}'")
        return True
    
    def read_house(self, house_name):
        print(f"Reading house '{house_name}'")
        return {"name": house_name, "metadata": {}, "rooms": []}
    
    def update_house(self, house_name, **metadata):
        print(f"Updating house '{house_name}' with metadata: {metadata}")
        return {"name": house_name, "updated_metadata": metadata}


class RoomAPI:
    def create_room(self, house_name, room_name, floor, size, **metadata):
        print(f"Creating room '{room_name}' on floor '{floor}' in house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": {"name": room_name, "floor": floor, "size": size, "metadata": metadata, "devices": []}}
    
    def delete_room(self, house_name, room_name):
        print(f"Deleting room '{room_name}' from house '{house_name}'")
        return True
    
    def read_room(self, house_name, room_name):
        print(f"Reading room '{room_name}' in house '{house_name}'")
        return {"house": house_name, "room": {"name": room_name, "metadata": {}, "devices": []}}
    
    def update_room(self, house_name, room_name, **metadata):
        print(f"Updating room '{room_name}' in house '{house_name}' with metadata: {metadata}")
        return {"house": house_name, "room": {"name": room_name, "updated_metadata": metadata}}


class UserAPI:
    def create_user(self, name, username, phone, email):
        print(f"Creating user '{username}' with name '{name}', phone '{phone}', and email '{email}'")
        return {"name": name, "username": username, "phone": phone, "email": email}
    
    def delete_user(self, username):
        print(f"Deleting user '{username}'")
        return True
    
    def read_user(self, username):
        print(f"Reading user '{username}'")
        return {"username": username, "name": "Example User", "phone": "0000000000", "email": "example@example.com"}
    
    def update_user(self, username, **attributes):
        print(f"Updating user '{username}' with attributes: {attributes}")
        return {"username": username, "updated_attributes": attributes}
