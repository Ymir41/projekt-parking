from Trackable import Trackable

class Car(Trackable):
    """
    A class of cars. It holds the plate number, it's location touple (x, y) and box - touple (x1, y1, x2, y2) with positions of
    upper right corner and bottom left corner.
    """
    def __init__(self, plate:str, location, box) -> None:
        self.plate = plate
        super().__init__(location, box)


