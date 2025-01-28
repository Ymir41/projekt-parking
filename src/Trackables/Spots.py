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

    def parked(self, cars: Cars) -> dict:
        """
        Determines which parking spots are taken and by which car.
        :param cars: A Cars object that has the cars to determine which are parked and where.
        :return: dictionary - key: a spot number, value: 1 if taken, 0 if free, -1 if incorrectly parked
        """
        spots = {}
        for number, spot in self.__spots.items():
            car_index = cars.getCarIndexOfLocation(spot.getBox())

            if not car_index is None:
                spots[number] = car_index
            else:
                spots[number] = -2

        indexes = []
        seen = {}

        for idx, value in spots.items():
            if value == -2:
                continue
            if value in seen:
                indexes.append(idx)
                if seen[value] is not None:
                    indexes.append(seen[value])
                    seen[value] = None  # Mark as already added
            else:
                seen[value] = idx

        for idx in spots.keys():
            if idx in indexes:
                spots[idx] = -1
            elif spots[idx] == -2:
                spots[idx] = 0
            else:
                spots[idx] = 1

        return spots

    def __len__(self) -> int:
        return len(self.__spots)

    def __getitem__(self, index: int) -> Spot:
        return self.__spots[index]

    def __bool__(self) -> bool:
        return len(self.__spots) > 0

    def scale(self, dims_old, dims_new):
        for indx in self.__spots.keys():
            spot = self.__spots[indx]
            box = spot.getBox()
            box.scale(dims_old, dims_new)
            self.__spots[indx] = Spot(indx, box)
