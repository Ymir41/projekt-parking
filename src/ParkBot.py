from  Signal import Signal
import cv2

class ParkBot(object):
    def __init__(self, cam) -> None:
        self.cam = cam
        self.checkCar = None
        self.carParked = Signal() # plate:str, spot: int
        self.carUnparked = Signal() # place:str, spot: int
        self.carAllowedToEnter = Signal() # plate:str
        self.carAllowedToExit = Signal() # plate:str
        self.carEntered = Signal() # plate:str
        self.carExited = Signal() # plate:str

    def setCheckCar(self, func):
        self.checkCar = func

    def __call__(self):
        pass


