import json

import cv2

from src.Trackers.Tracker import Tracker
from src.Trackables.Spots import Spots, Spot
from src.Trackables.Box import Box

class SpotTracker(Tracker):
    """
    Determines where parking spots are.
    """
    def __init__(self, spots:Spots) -> None:
        """
        :param spots: a Spots object to which the spots found in an image will be stored.
        """
        self.spots = spots

    def loadSpots(self, filename:str) -> None:
        with open(filename, "r") as f:
            data = json.load(f)

        for key, val in data.items():
            number = int(key.replace("box", ""))
            box = Box.from2Corners(*val)
            self.spots.append(Spot(number, box))


if __name__ == "__main__":
    spots = Spots()
    st = SpotTracker(spots)
    st.loadSpots("../../spot-config.json")
    image = cv2.imread("/home/janek/Documents/university/sem5/PSiO/projekt-parking/img3/20241223_123425.jpg")
    image = image / 255
    colors = {1:[0,0,1.0], 2:[0,0,1.0], 3:[0,0,1.0], 4:[0,0,1.0], 5:[0,0,1.0], 6:[0,0,1.0], 7:[0,0,1.0], 8:[0,0,1.0], 9:[0,0,1.0], 10:[0,0,1.0], 11:[0,0,1.0], 12:[0,0,1.0], 13:[0,0,1.0], 14:[0,0,1.0], 15:[0,0,1.0] }

    image = spots.draw(image, colors)
    print(image.shape)
    cv2.imshow("window", cv2.resize(image, (300, 400)))
    cv2.waitKey(0)

