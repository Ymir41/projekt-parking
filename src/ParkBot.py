from  Signal import Signal
import cv2
import numpy as np
from Trackers.CarTracker import CarTracker
from Trackers.SpotTracker import SpotTracker
from Trackables.Cars import Cars
from Trackables.Spots import Spots
from src.Trackers.EntryTracker import EntryTracker


class ParkBot(object):
    """
    A Class that monitors all relevant changes on the parking
    and announces them through Signals.
    """
    def __init__(self, cap: cv2.VideoCapture) -> None:
        """
        :param cap: a cv2.VideoCapture video of parking
        """
        self.cap = cap
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.checkCar = None
        self.carParked = Signal() # plate:str, spot: int
        self.carUnparked = Signal() # place:str, spot: int
        self.carAllowedToEnter = Signal() # plate:str
        self.carAllowedToExit = Signal() # plate:str
        self.readyToCloseEntryGate = Signal()
        self.readyToCloseExitGate = Signal()
        self.carEntered = Signal() # plate:str
        self.carExited = Signal() # plate:str
        self.imageRead = Signal() # img:np.ndarray
        self.imageTracked = Signal() # trackedImg:np.ndarray

        self.cars = Cars((self.height, self.width))
        self.spots = Spots()
        self.carTracker = CarTracker(self.cars)
        self.spotTracker = SpotTracker(self.spots)
        self.entryTracker = EntryTracker(self.checkCar, self.carAllowedToEnter, self.readyToCloseEntryGate);
        self.parkingState = {} # contains parkingSpot:carPlate

    def setCheckCar(self, func) -> None:
        """
        Sets the function used to determine whether car of given plate is allowed in.
        :param func: a function used to determine whether car of given plate number is allowed in.
        """
        self.checkCar = func
        self.entryTracker.isCarAllowed = func

    def __call__(self):
        pass

    def parkingDiffSpots(self, oldParkingState, newParkingState)->list:
        ""
        return []

