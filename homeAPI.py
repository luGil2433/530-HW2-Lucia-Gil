from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)  # Initialize Swagger for API documentation

# In-memory storage
data = {
    "users": [],
    "houses": [],
    "rooms": [],
    "devices": []
}

class UserResource(Resource):
    def post(self):
        """
        Add a new user
        ---
        tags:
          - Users
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                username:
                  type: string
                phone:
                  type: string
                email:
                  type: string
        responses:
          201:
            description: User added successfully
        """
        user = request.get_json()
        data["users"].append(user)
        return {"message": "User added successfully", "user": user}, 201

    def get(self):
        """
        Get all users
        ---
        tags:
          - Users
        responses:
          200:
            description: List of users
        """
        return {"users": data["users"]}, 200

class HouseResource(Resource):
    def post(self):
        """
        Add a new house
        ---
        tags:
          - Houses
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                address:
                  type: string
                gps_location:
                  type: string
        responses:
          201:
            description: House added successfully
        """
        house = request.get_json()
        data["houses"].append(house)
        return {"message": "House added successfully", "house": house}, 201

    def get(self):
        """
        Get all houses
        ---
        tags:
          - Houses
        responses:
          200:
            description: List of houses
        """
        return {"houses": data["houses"]}, 200

class RoomResource(Resource):
    def post(self):
        """
        Add a new room (must belong to a house)
        ---
        tags:
          - Rooms
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                floor:
                  type: integer
                size:
                  type: string
                house_name:
                  type: string
        responses:
          201:
            description: Room added successfully
          400:
            description: House name is required
        """
        room = request.get_json()
        if "house_name" not in room:
            return {"error": "House name is required"}, 400
        data["rooms"].append(room)
        return {"message": "Room added successfully", "room": room}, 201

    def get(self):
        """
        Get all rooms
        ---
        tags:
          - Rooms
        responses:
          200:
            description: List of rooms
        """
        return {"rooms": data["rooms"]}, 200

class DeviceResource(Resource):
    def post(self):
        """
        Add a new device (must belong to a room)
        ---
        tags:
          - Devices
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                type:
                  type: string
                name:
                  type: string
                room_name:
                  type: string
        responses:
          201:
            description: Device added successfully
          400:
            description: Room name is required
        """
        device = request.get_json()
        if "room_name" not in device:
            return {"error": "Room name is required"}, 400
        data["devices"].append(device)
        return {"message": "Device added successfully", "device": device}, 201

    def get(self):
        """
        Get all devices
        ---
        tags:
          - Devices
        responses:
          200:
            description: List of devices
        """
        return {"devices": data["devices"]}, 200

# Add resources to API with their respective routes
api.add_resource(UserResource, "/users")
api.add_resource(HouseResource, "/houses")
api.add_resource(RoomResource, "/rooms")
api.add_resource(DeviceResource, "/devices")

if __name__ == "__main__":
    app.run(debug=True)
