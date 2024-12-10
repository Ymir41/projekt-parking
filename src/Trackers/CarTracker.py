import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/Trackables"))) 

from Tracker import Tracker
from Trackables.Cars import Cars

class CarTracker(Tracker):
    def __init__(self, cars) -> None:
        self.cars = cars

    def track(self, img):
        pass

    def getCarPlate(self, carImg:np.ndarray):
        pass
