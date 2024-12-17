from src.Signal import Signal

class Trackable(object):
    def __init__(self, location, box) -> None:
        self.location = location 
        self.box = box
        self.moved = Signal() # location: tuple

    def move(self, new_location, new_box) -> None:
        self.location = new_location
        self.box = new_box
        self.moved.emit(new_location)
