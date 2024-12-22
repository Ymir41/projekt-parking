import numpy as np
from Tracker import Tracker

from src.Trackables.Spots import Spots, Spot

class SpotTracker(Tracker):
    """
    Determines where parking spots are.
    """
    def __init__(self, spots:Spots) -> None:
        """
        :param spots: a Spots object to which the spots found in an image will be stored.
        """
        self.spots = spots

    def track(self, img) -> None:
        """
        Looks for parking spots on an image (img) and saves there locations to self.spots
        :param img: image where with the spots to locate
        """
        pass

    def getSpotNumber(self, spotImg:np.ndarray) -> int:
        """
        It reads the spot number from an image of single spot. It determines the orientation of that spot.
        :param spotImg: a fragment of image with one spot.
        :return: int - a number of that spot
        """
        pass
