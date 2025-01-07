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
        # Recreate each Car with a new Box object based on the original Box's points
        out.__cars = [Car(car.label, Box(car.getBox().p[0][0], car.getBox().p[0][1],
                                         car.getBox().p[1][0], car.getBox().p[1][1],
                                         car.getBox().p[2][0], car.getBox().p[2][1],
                                         car.getBox().p[3][0], car.getBox().p[3][1])) for car in self.__cars]
        # Rebuild the locations array based on the new Boxes
        out.__locations = np.full(self.__dimensions, -1, dtype=int)
        for i, car in enumerate(out.__cars):
            box = car.getBox()
            mask = box.getMask(self.__dimensions)
            out.__locations[mask] = i
        return out

    def getDimensions(self):
        return self.__dimensions

    def getCarOfLocation(self, x: int, y: int):
        # Sprawdź, czy x i y są w zakresie wymiarów tablicy
        if x >= 0 and y >= 0 and y < self.__dimensions[0] and x < self.__dimensions[1]:
            if self.__locations[y, x] == -1:
                return None
            return self.__cars[self.__locations[y, x]]
        else:
            return None

    def updateCarsPositions(self, new_cars: 'Cars') -> None:
        """
        Updates positions and boxes of cars it holds based on the new positions found in new_cars,
        matching them by index order.
        :param new_cars: A Cars object with cars with new locations and boxes.
        """
        # Iterate through the new cars and update positions
        for i, new_car in enumerate(new_cars):
            if i < len(self.__cars):
                # Update existing car's box if the index is within current car list
                self.__cars[i].move(new_car.getBox())
            else:
                # Append new car if the index exceeds current car list
                self.append(new_car)

    def __updateLocations(self, car: 'Car') -> None:
        """
        Updates the location grid for a specific car.
        :param car: The car that has been moved and needs its grid location updated.
        """
        index = self.__cars.index(car)
        new_mask = car.getBox().getMask(self.__dimensions)
        self.__locations[new_mask] = index

    def getIndexFromPlate(self, plate: str) -> int:
        """
        Returns Index of car with given plate number. None if not found.
        :param plate: plate number of a car
        :return int: index of that car in self.__cars list
        """
        return [car.label for car in self.__cars].index(plate)

    def moveCar(self, index: int, new_box: Box) -> None:
        """Allows to move car to the new location"""
        if index >= len(self.__cars) or index < 0:
            raise IndexError("Index out of range")

        car = self.__cars[index]
        old_box = car.getBox()

        # Clear the old location in the __locations array
        old_mask = old_box.getMask(self.__dimensions)
        self.__locations[old_mask] = -1

        # Check if the new location is available
        new_mask = new_box.getMask(self.__dimensions)
        if np.any(self.__locations[new_mask] != -1):
            raise ValueError("New location is already occupied")

        # Move the car to the new location
        car.box = new_box
        self.__locations[new_mask] = index

    def moveCarByPlate(self, plate: str, new_box: Box) -> bool:
        """Allows to move car of given plate to the new location"""
        self.moveCar(self.getIndexFromPlate(plate), new_box)

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
        if index>len(self.__cars):
            raise IndexError("Index out of range")

        self.__locations = np.where(self.__locations == index, -1, self.__locations)
        self.__locations = np.where(self.__locations > index, self.__locations-1, self.__locations)
        del self.__cars[index]

    def removeByPlate(self, plate:str):
        """
        Removes car of given plate number from its self (this instance of Cars class, does not affect any database).
        :param plate: plate number of car to be removed
        """
        index = self.getIndexFromPlate(plate)
        if index is None:
            raise ValueError("Car of this plate does not exist.")
        self.__remove(self.getIndexFromPlate(plate))

    def getPlateFromIndex(self, index: int) -> str:
        return self.__cars[index].label


