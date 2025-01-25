from src.Trackables.Cars import Cars
from src.Trackables.Spot import Spot
from src.Trackables.TrackableCollection import TrackableCollection

class Spots(TrackableCollection):
    """
    It holds parking spots.
    """
    def __init__(self) -> None:
        self.__spots = {}

    def items(self):
        return self.__spots.items()

    def trackables(self) -> list[tuple[any, any]]:
        return [(spot.label, spot.getBox()) for spot in self.__spots.values()]

    def append(self, spot: Spot) -> None:
        """
        :param spot: A spot to be added.
        """
        self.__spots[spot.label] = spot

    def remove(self, index: int):
        del self.__spots[index]

    def parkedCars(self, cars: Cars) -> dict:
        """
        Determines which parking spots are taken and by which car.
        :param cars: A Cars object that has the cars to determine which are parked and where.
        :return: dictionary - key: a spot number, value: a car plate number
        """
        spots = {}
        for number, spot in self.items():
            location = spot.getLocation()
            car = cars.getCarOfLocation(*location)
            if car is None:
                spots[number] = None
            else:
                spots[number] = car.label
        return spots

    def __len__(self) -> int:
        return len(self.__spots)

    def __getitem__(self, index: int) -> Spot:
        return self.__spots[index]

    def __bool__(self) -> bool:
        return len(self.__spots)>0

