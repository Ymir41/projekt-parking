from src.Trackables.Box import Box
from typing_extensions import Self

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

    def setBox(self, new_box: Box):
        self.__box = new_box

    def getLocation(self):
        return self.getBox().middle()

    def getLabel(self):
        return self.label

    def setLabel(self, new_label: str):
        self.label = new_label

    def __eq__(self, other: Self):
        if not isinstance(other, Trackable):
            return NotImplemented
        return self.getBox() == other.getBox()
