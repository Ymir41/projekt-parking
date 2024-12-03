from Cars import Cars
from Spot import Spot

class Spots(object):
    def __init__(self) -> None:
        self.spots = {}
    
    def append(self, spot: Spot):
        self.spots[spot.number] = Spot

    def parkedCars(self) -> dict:
        pass

    def __sizeof__(self) -> int:
        return len(self.spots)

    def __getitem__(self, index: int) -> Spot:
        return self.spots[index]


