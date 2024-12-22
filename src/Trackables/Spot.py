from src.Trackables.Trackable import Trackable

class Spot(Trackable):
    """
    A class of parking spot. It holds the spot number and box - tuple (x1, y1, x2, y2) with positions of
    upper left corner and bottom right corner.
    """
    def __init__(self, number: int, box: tuple[int, int, int, int]) -> None:
        """
        :param number: the number of that spot
        :param box: the box around that spot (x1, y1, x2, y2) - upper left and bottom right corners
        """
        self.number = number
        super().__init__(box)
