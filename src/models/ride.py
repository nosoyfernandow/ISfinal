class Ride:
    def __init__(self, ride_id, ride_date_time, final_address, allowed_spaces, driver_alias):
        self.id = ride_id
        self.rideDateAndTime = ride_date_time
        self.finalAddress = final_address
        self.allowedSpaces = allowed_spaces
        self.driver = driver_alias
        self.status = "ready"  # ready, inprogress, done
        self.participants = []

    def to_dict(self):
        return {
            "id": self.id,
            "rideDateAndTime": self.rideDateAndTime,
            "finalAddress": self.finalAddress,
            "driver": self.driver,
            "status": self.status,
            "participants": [p.to_dict() for p in self.participants]
        }