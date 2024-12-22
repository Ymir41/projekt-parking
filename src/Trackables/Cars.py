import numpy as np
from Car import Car
from typing_extensions import Self

class Cars(object):
    """
    It holds cars on the parking.
    """

    def __init__(self, dimencions: tuple[2]) -> None:
        self.__cars = []
        self.__dimencions = dimencions
        self.__locations = np.zeros(dimencions) - 1

    def __iter__(self):
        return self.__cars.__iter__()

    def __sizeof__(self) -> int:
        return len(self.__cars)

    def __getitem__(self, index: int) -> Car:
        return self.__cars[index]

    def __getitem__(self, plate: str) -> Car:
        return self.__cars[index]

    def __setitem__(self, index: int, value: Car):
        pass

    def __bool__(self) -> bool:
        return len(self.__cars) > 0

    def updateCarsPositions(self, cars: Self) -> None:
        """
        Updates positions and boxes of cars it holds based to the new positions found in cars.
        When they have the same plate number then it is used to determine which cars are the same.
        Uses proximity of locations and boxes when plate number not given.
        :param cars: A Cars object with cars with new locations and boxes.
        """
        pass

    def getIndexFromPlate(self, plate: str) -> int:
        """
        Returnes Index of car with given plate number. None if not found.
        :param plate: plate number of a car
        :return int: index of that car in self.__cars list
        """
        pass

    def __moveCar(self, index: int, new_location: tuple[2], new_box: tuple[4]) -> bool:
        """Allows to move car to the new location"""
        pass

    def moveCarByPlate(self, plate: str, new_location: tuple[2], new_box: tuple[4]) -> bool:
        """Allows to move car of given plate to the new location"""
        pass

    def append(self, car: Car) -> None:
        """
        Adds new car to this instance of Cars class (does not affect any database).
        :param car: a Car object to be added
        """
        self.__cars.append(car)
        self.__locations[car.location] = len(self.__cars)

    def __remove(self, index: int) -> None:
        """
        :param index: index in self.__cars of car to be removed
        """

    def removeByPlate(self, plate:str):
        """
        Removes car of given plate number from its self (this instance of Cars class, does not affect any database).
        :param plate: plate number of car to be removed
        :return:
        """
        pass

    def getPlate(self, index: int) -> str:
        return self.__cars[index].plate


