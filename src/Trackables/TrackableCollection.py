from src.Trackables.Trackable import Trackable, Box
import numpy as np

class TrackableCollection(object):
    def trackables(self) -> list[tuple[any, any]]:
        pass

    def draw(self, img: np.ndarray) -> np.ndarray:
        for label, box in self.trackables():
            pass