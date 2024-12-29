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

    def __copy__(self):
        out = self.__class__(self.label, self.getBox())
        return out

    @restrict_access("Cars")
    def move(self,  new_box: Box) -> None:
        """
        Moves the object around the image.
        :param new_location: the new location of the Trackable (x, y)
        :param new_box: the new box around the trackable (x1, y1, x2, y2)
        """
        self.__box = new_box
