from src.Trackables.Trackable import Trackable
from src.restrict_acces import restrict_access


class Car(Trackable):
    """
    A class of cars. It holds the plate number, it's location tuple (x, y) and box - tuple (x1, y1, x2, y2) with positions of
    upper left corner and bottom right corner.
    The location is calculated based on box.
    """
    def __init__(self, plate:str|None, box: tuple[int, int, int, int]) -> None:
        """
        :param plate: plate number (can be None)
        :param box: box around the car (x1, y1, x2, y2) - upper left and bottom right corners
        """
        self.plate = plate
        super().__init__(box)

    def __copy__(self):
        out = self.__class__(self.plate, self.getBox())
        return out

    @restrict_access("Cars")
    def move(self,  new_box: tuple[int, int, int, int]) -> None:
        """
        Moves the object around the image.
        :param new_location: the new location of the Trackable (x, y)
        :param new_box: the new box around the trackable (x1, y1, x2, y2)
        """
        self.__setBox(new_box)
