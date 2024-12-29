import numpy as np
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
        self.__locations:np.ndarray = np.zeros(dimensions, dtype=int) - 1

    def __iter__(self):
        return self.__cars.__iter__()

    def __getitem__(self, index: int|str) -> Car:
        if type(index) == int:
            return self.__cars[index]
        elif type(index) == str:
            return self.__cars[self.getIndexFromPlate(index)]

    def __bool__(self) -> bool:
        return len(self.__cars) > 0

    def __len__(self):
        return len(self.__cars)

    def trackables(self) -> list[tuple[any, any]]:
            return [(car.label, car.getBox()) for car in self.__cars]

    def copy(self) -> Self:
        """
        :return Cars: copy of itself
        """
        out = Cars(self.__dimensions)
        out.__locations = self.__locations.copy()
        out.__cars = self.__cars.copy()
        return out

    def getDimensions(self):
        return self.__dimensions

    def getCarOfLocation(self, x:int, y:int):
        if self.__locations[y, x] == -1:
            return None
        return self.__cars[self.__locations[y, x]]

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
        Returns Index of car with given plate number. None if not found.
        :param plate: plate number of a car
        :return int: index of that car in self.__cars list
        """
        return [car.label for car in self.__cars].index(plate)

    def moveCar(self, index: int, new_box: tuple[int, int, int, int]) -> None:
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
        if self.getCarOfLocation(*car.getLocation()) != None:
            raise ValueError("Car of with location already occupied")

        self.__cars.append(car)
        box = car.getBox()
        mask = box.getMask(self.__locations.shape)
        self.__locations[mask] = len(self.__cars) - 1

    def __remove(self, index: int) -> None:
        """
        :param index: index in self.__cars of car to be removed
        """
        pass

    def removeByPlate(self, plate:str):
        """
        Removes car of given plate number from its self (this instance of Cars class, does not affect any database).
        :param plate: plate number of car to be removed
        :return:
        """
        pass

    def getPlateFromIndex(self, index: int) -> str:
        return self.__cars[index].label


