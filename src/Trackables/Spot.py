from Trackable import Trackable

class Spot(Trackable):
    def __init__(self, number, location, box) -> None:
        self.number = number
        super().__init__(location, box)
