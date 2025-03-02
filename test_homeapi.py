import unittest
from models import DeviceAPI, HouseAPI, RoomAPI, UserAPI

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.api = UserAPI()

    def test_create_user_success(self):
        result = self.api.create_user(
            "John Doe", 
            "johndoe", 
            "+1234567890", 
            "john@example.com"
        )
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["username"], "johndoe")
        self.assertEqual(result["phone"], "+1234567890")
        self.assertEqual(result["email"], "john@example.com")

    def test_create_user_invalid_phone(self):
        with self.assertRaises(ValueError):
            self.api.create_user(
                "John Doe", 
                "johndoe", 
                "invalid-phone", 
                "john@example.com"
            )

    def test_create_user_invalid_email(self):
        with self.assertRaises(ValueError):
            self.api.create_user(
                "John Doe", 
                "johndoe", 
                "+1234567890", 
                "invalid-email"
            )

    def test_read_user(self):
        result = self.api.read_user("johndoe")
        self.assertIn("username", result)
        self.assertIn("name", result)
        self.assertIn("phone", result)
        self.assertIn("email", result)

    def test_update_user(self):
        result = self.api.update_user("johndoe", phone="+9876543210")
        self.assertEqual(result["username"], "johndoe")
        self.assertEqual(result["updated_attributes"]["phone"], "+9876543210")

    def test_delete_user(self):
        result = self.api.delete_user("johndoe")
        self.assertTrue(result)

class TestHouseAPI(unittest.TestCase):
    def setUp(self):
        self.api = HouseAPI()

    def test_create_house_success(self):
        result = self.api.create_house(
            "Smart Home", 
            address="123 Main St",
            gps_location="40.7128,-74.0060"
        )
        self.assertEqual(result["name"], "Smart Home")
        self.assertEqual(result["metadata"]["address"], "123 Main St")
        self.assertEqual(result["metadata"]["gps_location"], "40.7128,-74.0060")

    def test_create_house_no_name(self):
        with self.assertRaises(ValueError):
            self.api.create_house("")

    def test_read_house(self):
        result = self.api.read_house("Smart Home")
        self.assertIn("name", result)
        self.assertIn("metadata", result)
        self.assertIn("rooms", result)

    def test_update_house(self):
        result = self.api.update_house(
            "Smart Home", 
            address="456 New St"
        )
        self.assertEqual(result["name"], "Smart Home")
        self.assertEqual(result["updated_metadata"]["address"], "456 New St")

    def test_delete_house(self):
        result = self.api.delete_house("Smart Home")
        self.assertTrue(result)

class TestRoomAPI(unittest.TestCase):
    def setUp(self):
        self.api = RoomAPI()

    def test_create_room_success(self):
        result = self.api.create_room(
            "Smart Home",
            "Living Room",
            1,
            "Large",
            color="Blue"
        )
        self.assertEqual(result["house"], "Smart Home")
        self.assertEqual(result["room"]["name"], "Living Room")
        self.assertEqual(result["room"]["floor"], 1)
        self.assertEqual(result["room"]["size"], "Large")
        self.assertEqual(result["room"]["metadata"]["color"], "Blue")

    def test_create_room_invalid_floor(self):
        with self.assertRaises(ValueError):
            self.api.create_room(
                "Smart Home",
                "Living Room",
                "invalid_floor",
                "Large"
            )

    def test_read_room(self):
        result = self.api.read_room("Smart Home", "Living Room")
        self.assertIn("house", result)
        self.assertIn("room", result)
        self.assertIn("devices", result["room"])

    def test_update_room(self):
        result = self.api.update_room(
            "Smart Home",
            "Living Room",
            color="Green"
        )
        self.assertEqual(result["house"], "Smart Home")
        self.assertEqual(result["room"]["name"], "Living Room")
        self.assertEqual(result["room"]["updated_metadata"]["color"], "Green")

    def test_delete_room(self):
        result = self.api.delete_room("Smart Home", "Living Room")
        self.assertTrue(result)

class TestDeviceAPI(unittest.TestCase):
    def setUp(self):
        self.api = DeviceAPI()

    def test_create_device_success(self):
        result = self.api.create_device(
            "Smart Home",
            "Living Room",
            "Light",
            "Ceiling Light",
            brightness=80
        )
        self.assertEqual(result["house"], "Smart Home")
        self.assertEqual(result["room"], "Living Room")
        self.assertEqual(result["device"]["type"], "Light")
        self.assertEqual(result["device"]["name"], "Ceiling Light")
        self.assertEqual(result["device"]["metadata"]["brightness"], 80)

    def test_create_device_missing_required_fields(self):
        with self.assertRaises(ValueError):
            self.api.create_device("", "Living Room", "Light", "Ceiling Light")

    def test_read_device(self):
        result = self.api.read_device(
            "Smart Home",
            "Living Room",
            "Ceiling Light"
        )
        self.assertIn("house", result)
        self.assertIn("room", result)
        self.assertIn("device", result)
        self.assertIn("data", result["device"])

    def test_update_device(self):
        result = self.api.update_device(
            "Smart Home",
            "Living Room",
            "Ceiling Light",
            brightness=100
        )
        self.assertEqual(result["house"], "Smart Home")
        self.assertEqual(result["room"], "Living Room")
        self.assertEqual(result["device"]["name"], "Ceiling Light")
        self.assertEqual(result["device"]["updated_metadata"]["brightness"], 100)

    def test_delete_device(self):
        result = self.api.delete_device(
            "Smart Home",
            "Living Room",
            "Ceiling Light"
        )
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()