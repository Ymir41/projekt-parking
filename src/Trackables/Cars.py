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

    def __iter__(self):
        return self.__cars.__iter__()

    def __getitem__(self, index: int | str) -> Car:
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

    @classmethod
    def boxListToCars(cls, boxList:list, dim:tuple[int, int]):
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

    def copy(self) -> Self:
        """
        :return Cars: copy of itself
        """
        out = Cars(self.__dimensions)
        # Recreate each Car with a new Box object based on the original Box's points
        out.__cars = [car.copy_() for car in self.__cars]
        # Rebuild the locations array based on the new Boxes
        out.__locations = self.__locations.copy()

        return out

    def getDimensions(self):
        return self.__dimensions

    def getCarOfLocation(self, x: int, y: int):
        """
        Returns car located at specific location (x, y).
        """
        # Sprawdź, czy współrzędne są w zakresie
        if x < 0 or y < 0 or y >= self.__dimensions[0] or x >= self.__dimensions[1]:
            return None

        # Pobierz wartość indeksu z lokalizacji
        location_index = self.__locations[y, x]

        # Sprawdź, czy lokalizacja jest pusta lub indeks jest poza zakresem
        if any(location_index == -1) or not all(0 <= int(x) < len(self.__cars) for x in location_index):
            return None

        return self.__cars[int(location_index)]


    def updateCarsPositions(self, new_cars: 'Cars') -> None:
        """
        Updates positions and boxes of cars it holds based on the new positions found in new_cars,
        matching them by index order.
        :param new_cars: A Cars object with cars with new locations and boxes.
        """
        unlabeled_cars = []
        unlabeled_cars_number_of_matches = {}
        plates = [car.getPlate() for car in self.__cars]
        plates = plates.copy()
        cars = self.__cars.copy()
        unmoved = dict(zip(plates, cars))
        # Iterate through the new cars and update positions
        for i, new_car in enumerate(new_cars):
            plate = new_car.getPlate()
            if plate is None:
                unlabeled_cars.append(new_car)
                continue
            if plate not in plates:
                self.append(new_car)
                continue
            index = self.getIndexFromPlate(plate)
            # Update existing car's box if the index is within current car list
            self.__cars[index].move(new_car.getBox())
            del unmoved[plate]

        for new_car in unlabeled_cars:
            potential_old_cars = list(filter(lambda car: car.getBox().withinRange(new_car.getBox()), unmoved.values()))
            unlabeled_cars_number_of_matches[new_car.getBox()] = len(potential_old_cars)

        unlabeled_cars.sort(key=lambda car: unlabeled_cars_number_of_matches[car.getBox()])

        for new_car in unlabeled_cars:
            potential_old_cars = list(filter(lambda car: car.getBox().withinRange(new_car.getBox()), unmoved.values()))
            if len(potential_old_cars) == 0:
                continue
            old_car = min(potential_old_cars, key=lambda car: car.getBox().distance(new_car.getBox()))
            old_car.move(new_car.getBox())
            del unmoved[old_car.getPlate()]

        for plate, old_car in unmoved.items():
            self.removeByPlate(plate)

        self.callculateLocations()

    def callculateLocations(self):
        self.__locations = np.zeros(self.__dimensions, dtype=int) * -1
        for i, car in enumerate(self.__cars):
            mask = car.getBox().getMask(self.__dimensions)
            if mask.any():  # Dodano zabezpieczenie przed pustymi maskami
                self.__locations[mask] = i

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
        car.setBox(new_box)
        self.__locations[new_mask] = index

    def moveCarByPlate(self, plate: str, new_box: Box) -> bool:
        """Allows to move car of given plate to the new location"""
        self.moveCar(self.getIndexFromPlate(plate), new_box)

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

    def __remove(self, index: int) -> None:
        """
        :param index: index in self.__cars of car to be removed
        """
        if index > len(self.__cars):
            raise IndexError("Index out of range")

        self.__locations = np.where(self.__locations == index, -1, self.__locations)
        self.__locations = np.where(self.__locations > index, self.__locations - 1, self.__locations)
        del self.__cars[index]

    def removeByPlate(self, plate: str):
        """
        Removes car of given plate number from its self (this instance of Cars class, does not affect any database).
        :param plate: plate number of car to be removed
        """
        index = self.getIndexFromPlate(plate)
        if index is None:
            raise ValueError("Car of this plate does not exist.")
        self.__remove(self.getIndexFromPlate(plate))

    def getPlateFromIndex(self, index: int) -> str:
        return self.__cars[index].getPlate()

    def getCarIndexOfLocation(self, spotBox: Box):
        """
        Returns index of car located at specific location (x, y).
        """

        for i, car in enumerate(self.__cars):
            midpoint_1 = ((car.getBox().p[0][0] + car.getBox().p[1][0]) // 2,
                          (car.getBox().p[0][1] + car.getBox().p[1][1]) // 2)  #0-1
            midpoint_2 = ((car.getBox().p[1][0] + car.getBox().p[2][0]) // 2,
                          (car.getBox().p[1][1] + car.getBox().p[2][1]) // 2)  #1-2
            midpoint_3 = ((car.getBox().p[2][0] + car.getBox().p[3][0]) // 2,
                          (car.getBox().p[2][1] + car.getBox().p[3][1]) // 2)  #2-3
            midpoint_4 = ((car.getBox().p[3][0] + car.getBox().p[0][0]) // 2,
                          (car.getBox().p[3][1] + car.getBox().p[0][1]) // 2)  #3-0

            if spotBox.inside(car.getLocation()) \
                    or spotBox.inside(midpoint_1) \
                    or spotBox.inside(midpoint_2) \
                    or spotBox.inside(midpoint_3) \
                    or spotBox.inside(midpoint_4):
                return i

