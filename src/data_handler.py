import json
from src.models.usuario import User
from src.models.ride import Ride
from src.models.rideparticipation import RideParticipation


class DataHandler:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.users = []
        self.rides = []
        self.load_data()

    def save_data(self):
        data = {
            'users': [u.__dict__ for u in self.users],
            'rides': [self.serialize_ride(r) for r in self.rides]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.users = [User(**u) for u in data.get('users', [])]
                self.rides = [self.deserialize_ride(r) for r in data.get('rides', [])]
        except FileNotFoundError:
            self.users = []
            self.rides = []

    def serialize_ride(self, ride):
        return {
            "id": ride.id,
            "rideDateAndTime": ride.rideDateAndTime,
            "finalAddress": ride.finalAddress,
            "allowedSpaces": ride.allowedSpaces,
            "driver": ride.driver,
            "status": ride.status,
            "participants": [p.__dict__ for p in ride.participants]
        }

    def deserialize_ride(self, data):
        ride = Ride(
            ride_id=data["id"],
            ride_date_time=data["rideDateAndTime"],
            final_address=data["finalAddress"],
            allowed_spaces=data["allowedSpaces"],
            driver_alias=data["driver"]
        )
        ride.status = data.get("status", "ready")
        ride.participants = [RideParticipation(**p) for p in data.get("participants", [])]
        return ride
