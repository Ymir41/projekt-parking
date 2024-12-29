from src.Trackables.Cars import Cars
from src.Trackables.Spot import Spot

class Spots(object):
    """
    It holds parking spots.
    """
    def __init__(self) -> None:
        self.__spots = {}

    def items(self):
        return self.__spots.items()
    
    def append(self, spot: Spot) -> None:
        """
        :param spot: A spot to be added.
        """
        self.__spots[spot.label] = Spot

    def parkedCars(self, cars: Cars) -> dict:
        """
        Determines which parking spots are taken and by which car.
        :param cars: A Cars object that has the cars to determine which are parked and where.
        :return: dictionary - key: a spot number, value: a car plate number
        """
        pass

    def __len__(self) -> int:
        return len(self.__spots)

    def __getitem__(self, index: int) -> Spot:
        return self.__spots[index]

    def __bool__(self) -> bool:
        return len(self.__spots)>0

