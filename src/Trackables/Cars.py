import numpy as np
from exceptiongroup import catch

from src.Trackables.Car import Car, Box
from src.Trackables.TrackableCollection import TrackableCollection
from typing_extensions import Self


class Cars(TrackableCollection):
    """
    It holds cars on the parking.
    """

    def __init__(self, dimensions: tuple[int, int]) -> None:
        self.__cars = []
        self.__dimensions = dimensions
        self.__locations: np.ndarray = np.zeros(dimensions, dtype=int) - 1

    @classmethod
    def boxListToCars(cls, boxList: list, dim: tuple[int, int]):
        """
        Takes list of boxes and creates Cars object based on it
        :param boxList: list of Boxes to convert
        :param dim: dimensions of image
        :return: Cars - object with cars of boxes provided in boxList
        """
        out = Cars(dim)
        for box in boxList:
            car = Car("", box)
            out.append(car)
        return out

    def append(self, car: Car) -> None:
        """
        Adds new car to this instance of Cars class (does not affect any database).
        :param car: a Car object to be added
        """
        location = car.getLocation()

        # Upewnij się, że współrzędne są całkowite
        x, y = int(location[0]), int(location[1])

        self.__cars.append(car)

        # Dodaj nową lokalizację do maski
        box = car.getBox()
        mask = box.getMask(self.__locations.shape)
        self.__locations[mask] = len(self.__cars) - 1

    def getCarIndexOfLocation(self, spotBox: Box):
        """
        Returns index of car located at specific location (x, y).
        """

        for i, car in enumerate(self.__cars):
            midpoint_1 = ((car.getBox().p[0][0] + car.getBox().p[1][0]) // 2,
                          (car.getBox().p[0][1] + car.getBox().p[1][1]) // 2)  # 0-1
            midpoint_2 = ((car.getBox().p[1][0] + car.getBox().p[2][0]) // 2,
                          (car.getBox().p[1][1] + car.getBox().p[2][1]) // 2)  # 1-2
            midpoint_3 = ((car.getBox().p[2][0] + car.getBox().p[3][0]) // 2,
                          (car.getBox().p[2][1] + car.getBox().p[3][1]) // 2)  # 2-3
            midpoint_4 = ((car.getBox().p[3][0] + car.getBox().p[0][0]) // 2,
                          (car.getBox().p[3][1] + car.getBox().p[0][1]) // 2)  # 3-0

            if spotBox.inside(car.getLocation()) \
                    or spotBox.inside(midpoint_1) \
                    or spotBox.inside(midpoint_2) \
                    or spotBox.inside(midpoint_3) \
                    or spotBox.inside(midpoint_4):
                return i
