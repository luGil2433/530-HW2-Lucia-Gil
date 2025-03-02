from models import DeviceAPI, HouseAPI, RoomAPI, UserAPI

def main():
    user_api = UserAPI()
    house_api = HouseAPI()
    room_api = RoomAPI()
    device_api = DeviceAPI()
    

    print("Welcome to the Smart Home API!")
    while True:
        action = input("Do you want to create a new entity? ( type user, house, room or device for entering new entity), type '2' to run pre programed test, or type '0' to exsit: ").strip().lower()
        if action == "2":
            # Test User API
            print("\n--- Testing User API ---")
            user = user_api.create_user("John Doe", "johndoe", "+1234567890", "john@example.com")
            print(user_api.read_user("johndoe"))
            print(user_api.update_user("johndoe", phone="+0987654321"))
            print(user_api.delete_user("johndoe"))
            
            # Test House API
            print("\n--- Testing House API ---")
            house = house_api.create_house("My Smart Home", address="123 Main St", gps_location="40.7128,-74.0060")
            print(house_api.read_house("My Smart Home"))
            print(house_api.update_house("My Smart Home", address="456 Elm St"))
            print(house_api.delete_house("My Smart Home"))
            
            # Test Room API
            print("\n--- Testing Room API ---")
            room = room_api.create_room("My Smart Home", "Living Room", 1, "Large")
            print(room_api.read_room("My Smart Home", "Living Room"))
            print(room_api.update_room("My Smart Home", "Living Room", color="Blue"))
            print(room_api.delete_room("My Smart Home", "Living Room"))
            
            # Test Device API
            print("\n--- Testing Device API ---")
            device = device_api.create_device("My Smart Home", "Living Room", "Light", "Ceiling Light", brightness=80)
            print(device_api.read_device("My Smart Home", "Living Room", "Ceiling Light"))
            print(device_api.update_device("My Smart Home", "Living Room", "Ceiling Light", brightness=100))
            print(device_api.delete_device("My Smart Home", "Living Room", "Ceiling Light"))
            break
        elif action == "user":
            name = input("Enter full name: ")
            username = input("Enter username: ")
            phone = input("Enter phone number: ")
            email = input("Enter email: ")
            api = UserAPI()
            print(api.create_user(name, username, phone, email))
        elif action == "house":
            house_name = input("Enter house name: ")
            api = HouseAPI()
            print(api.create_house(house_name))
        elif action == "room":
            house_name = input("Enter house name: ")
            room_name = input("Enter room name: ")
            floor = int(input("Enter floor number: "))
            size = input("Enter room size: ")
            api = RoomAPI()
            print(api.create_room(house_name, room_name, floor, size))
        elif action == "device":
            house_name = input("Enter house name: ")
            room_name = input("Enter room name: ")
            device_type = input("Enter device type: ")
            device_name = input("Enter device name: ")
            api = DeviceAPI()
            print(api.create_device(house_name, room_name, device_type, device_name))
        elif action == "0":
            break
        else:
            print("Invalid option. Please enter 'user', 'house', 'room', or 'device'.")


if __name__ == "__main__":
    main()
