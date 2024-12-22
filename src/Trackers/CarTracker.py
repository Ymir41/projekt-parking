import numpy as np
import sys
import os


from src.Trackers.Tracker import Tracker
from src.Trackables.Cars import Cars

class CarTracker(Tracker):
    """
    Locates cars in an image and tracks them around the parking.
    """
    def __init__(self, cars: Cars) -> None:
        """
        :param cars: Cars object that holds the cars on the parking with their positions and boxes around them.
        """
        self.cars = cars

    def track(self, img: np.ndarray) -> None:
        """
        Updates the locations of the cars in self.cars with positions of cars found in the image.
        :param img: img with the new state of parking with cars to track.
        """
        pass

    def locate_cars(self, img: np.ndarray) -> Cars:
        """
        It locates cars on an image of parking and returns them with their positions and boxes.
        Cars returned do not have plate numbers.
        :param img: the image with cars to locate
        :return: Cars - a collection of cars found in the image.
        """
        pass

