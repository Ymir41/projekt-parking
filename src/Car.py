from Trackable import Trackable

class Car(Trackable):
    def __init__(self, plate:str, location, box) -> None:
        self.plate = plate
        super().__init__(location, box)


