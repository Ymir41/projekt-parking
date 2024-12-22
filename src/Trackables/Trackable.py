from src.Signal import Signal

class Trackable(object):
    """
    Abstract class of Trackable.
    """
    def __init__(self, location, box) -> None:
        self.__location = location
        self.__box = box
        self.__moved = Signal() # location: tuple

    def getBox(self):
        return self.__box

    def getLocation(self):
        return self.__location

    def move(self, new_location: tuple[2], new_box: tuple[4]) -> None:
        """
        Moves the object around the image.
        :param new_location: the new location of the Trackable (x, y)
        :param new_box: the new box around the trackable (x1, y1, x2, y2)
        """
        self.location = new_location
        self.box = new_box
        self.moved.emit(new_location)
