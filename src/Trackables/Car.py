from src.Trackables.Trackable import Trackable, Box


class Car(Trackable):
    """
    A class of cars. It holds the plate number, it's location tuple (x, y) and box - tuple (x1, y1, x2, y2) with positions of
    upper left corner and bottom right corner.
    The location is calculated based on box.
    """
    _id_counter = 0

    def __init__(self, plate: str, box: Box) -> None:
        """
        :param plate: plate number (can be None)
        :param box: box around the car (x1, y1, x2, y2) - upper left and bottom right corners
        """
        super().__init__(plate, box)
        self.id = Car._id_counter
        Car._id_counter += 1

    def getPlate(self):
        """Accessor method for the car's plate number."""
        return self.getLabel()

    def setPlate(self, plate: str):
        """Sets the plate number only if it hasn't been set before."""
        if self.getLabel() is None:
            self.setLabel(plate)

    def copy_(self):
        out = self.__class__(self.getPlate(), self.getBox())
        return out

