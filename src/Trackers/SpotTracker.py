import json

import cv2

from src.Trackers.Tracker import Tracker
from src.Trackables.Spots import Spots, Spot
from src.Trackables.Box import Box

class SpotTracker(Tracker):
    """
    Determines where parking spots are.
    """
    def __init__(self, spots:Spots) -> None:
        """
        :param spots: a Spots object to which the spots found in an image will be stored.
        """
        self.spots = spots

    def loadSpots(self, filename:str) -> None:
        with open(filename, "r") as f:
            data = json.load(f)

        for key, val in data.items():
            number = int(key.replace("box", ""))
            box = Box.from2Corners(*val)
            self.spots.append(Spot(number, box))


