class RideParticipation:
    def __init__(self, participant_alias, destination, occupied_spaces):
        self.participant = participant_alias
        self.confirmation = None
        self.destination = destination
        self.occupiedSpaces = occupied_spaces
        self.status = "waiting"  # waiting, rejected, confirmed, missing, notmarked, inprogress, done

    def to_dict(self):
        return {
            "participant": self.participant,
            "confirmation": self.confirmation,
            "destination": self.destination,
            "occupiedSpaces": self.occupiedSpaces,
            "status": self.status
        }
