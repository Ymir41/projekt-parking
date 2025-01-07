from src.Trackables.Trackable import Trackable, Box
from src.restrict_acces import restrict_access


class Car(Trackable):
    """
    A class of cars. It holds the plate number, it's location tuple (x, y) and box - tuple (x1, y1, x2, y2) with positions of
    upper left corner and bottom right corner.
    The location is calculated based on box.
    """
    def __init__(self, plate:str|None, box: Box) -> None:
        """
        :param plate: plate number (can be None)
        :param box: box around the car (x1, y1, x2, y2) - upper left and bottom right corners
        """
        super().__init__(plate, box)

    def getPlate(self):
        """Accessor method for the car's plate number."""
        return self.getLabel()

    def __copy__(self):
        out = self.__class__(self.label, self.getBox())
        return out

    def __str__(self):
        return f"Car(\"{self.label}\", {self.getBox()})"

    def __repr__(self):
        return self.__str__()

    # @restrict_access("Cars")
    def move(self,  new_box: Box) -> None:
        """
        Moves the object around the image.
        :param new_box: the new box around the trackable
        """
        self.box = new_box
