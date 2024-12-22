from src.Signal import Signal

class Trackable(object):
    """
    Abstract class of Trackable.
    """
    def __init__(self, box: tuple[int, int, int, int]) -> None:
        """
        :param box: a box around the object (x1, y1, x2, y2) - upper left and bottom right corners
        """
        self.__setBox(box)

    def __setBox(self, box: tuple[int, int, int, int]):
        self.__box = box
        self.__location = ((box[0]+box[2])//2, (box[1] + box[3])//2)

    def getBox(self):
        return self.__box

    def getLocation(self):
        return self.__location

