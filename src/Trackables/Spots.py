from Cars import Cars
from Spot import Spot

class Spots(object):
    def __init__(self) -> None:
        self.spots = {}

    def __iter__(self):
        return self.spots.values().__iter__()
    
    def append(self, spot: Spot):
        self.spots[spot.number] = Spot

    def parkedCars(self, cars: Cars) -> dict:
        pass

    def __sizeof__(self) -> int:
        return len(self.spots)

    def __getitem__(self, index: int) -> Spot:
        return self.spots[index]

    def __bool__(self) -> bool:
        return len(self.spots)>0

