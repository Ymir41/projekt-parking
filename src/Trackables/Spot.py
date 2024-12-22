from Trackable import Trackable

class Spot(Trackable):
    """
    A class of parking spot. It holds the spot number, it's location and box - touple (x1, y1, x2, y2) with positions of
    upper right corner and bottom left corner.
    """
    def __init__(self, number, location, box) -> None:
        self.number = number
        super().__init__(location, box)
