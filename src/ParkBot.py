from  Signal import Signal
import cv2
import numpy as np
from Trackers.CarTracker import CarTracker
from Trackers.SpotTracker import SpotTracker
from Trackables.Cars import Cars
from Trackables.Spots import Spots

class ParkBot(object):
    def __init__(self, cap) -> None:
        self.cap = cap
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.checkCar = None
        self.carParked = Signal() # plate:str, spot: int
        self.carUnparked = Signal() # place:str, spot: int
        self.carAllowedToEnter = Signal() # plate:str
        self.carAllowedToExit = Signal() # plate:str
        self.carEntered = Signal() # plate:str
        self.carExited = Signal() # plate:str
        self.imageRead = Signal() # img:np.ndarray
        self.imageTracked = Signal() # trackedImg:np.ndarray

        self.cars = Cars((self.height, self.width))
        self.spots = Spots()
        self.carTracker = CarTracker(self.cars)
        self.spotTracker = SpotTracker(self.spots)
        self.parkingState = {} # contains parkingSpot:carPlate
        self.threshold = np.zeros(3)
        self.tul = 0

    def setCheckCar(self, func):
        self.checkCar = func

    def __call__(self):
        pass

    def parkingDiffPlates(self, oldParkingState, newParkingState)->list:
        return []

