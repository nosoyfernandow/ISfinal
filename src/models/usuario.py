class User:
    def __init__(self, alias, name, car_plate=None):
        self.alias = alias
        self.name = name
        self.car_plate = car_plate
        self.rides = []  # ride participations

    def to_dict(self):
        return {
            "alias": self.alias,
            "name": self.name,
            "carPlate": self.car_plate
        }