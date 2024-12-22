from Cars import Cars
from Spot import Spot

class Spots(object):
    """
    It holds parking spots.
    """
    def __init__(self) -> None:
        self.spots = {}

    def __iter__(self):
        return self.spots.values().__iter__()
    
    def append(self, spot: Spot) -> None:
        """
        :param spot: A spot to be added.
        """
        self.spots[spot.number] = Spot

    def parkedCars(self, cars: Cars) -> dict:
        """
        Determines which parking spots are taken and by which car.
        :param cars: A Cars object that has the cars to determine which are parked and where.
        :return: dictionary - key: a spot number, value: a car plate number
        """
        pass

    def __sizeof__(self) -> int:
        return len(self.spots)

    def __getitem__(self, index: int) -> Spot:
        return self.spots[index]

    def __bool__(self) -> bool:
        return len(self.spots)>0

