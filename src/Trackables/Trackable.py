from src.Signal import Signal
from src.Trackables.Box import Box

class Trackable(object):
    """
    Abstract class of Trackable.
    """
    def __init__(self, label, box: Box) -> None:
        """
        :param box: a box around the object (x1, y1, x2, y2) - upper left and bottom right corners
        """
        self.__box = box
        self.label = label

    def getBox(self):
        return self.__box

    def getLocation(self):
        return self.__box.middle()

