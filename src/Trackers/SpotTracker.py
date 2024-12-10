import numpy as np
from Tracker import Tracker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 

from Trackables.Spots import Spots




class SpotTracker(Tracker):
    def __init__(self, spots:Spots) -> None:
        self.spots = spots

    def track(self, img):
        pass

    def getSpotNumber(self, spotImg:np.ndarray):
        pass
