import numpy as np
from Car import Car

class Cars(object):
    def __init__(self, dims) -> None:
        self.cars = []
        self.dims = dims
        self.locations = np.zeros(dims)-1

    def __iter__(self):
        return self.cars.__iter__()

    def moveCar(self, index, new_location):
        pass

    def append(self, car: Car):
        self.cars.append(car)
        self.locations[car.location] = len(self.cars)

    def removeByPlate(self, plate:str):
        pass

    def getPlate(self, index: int) -> str:
        return self.cars[index].plate

    def __sizeof__(self) -> int:
        return len(self.cars)

    def __getitem__(self, index: int) -> Car:
        return self.cars[index]

    def __setitem__(self, index: int, value: Car):
        pass

    def __bool__(self) -> bool:
        return len(self.cars)>0

