from src.Trackables.Trackable import Trackable, Box
import numpy as np
import cv2

class TrackableCollection(object):
    def trackables(self) -> list[tuple[int|str, Box]]: # implemented in each class
        pass

    def draw(self, img: np.ndarray, colors: dict[str, tuple[float, float, float]]) -> np.ndarray:
        """
        Draws a box with label on top on provided opencv image. For each label uses color from dictionary colors.
        :param img: np.ndarray with image (B,G,R). An image on witch it will draw.
        :param colors: dictionary with colors for each label - colors as tuple in BGR format
        :return: np.ndarray an image with boxes of that TrackableCollection drawn on.
        """
        for label, box in self.trackables():
            color = colors[label]
            img = cv2.rectangle(img, box.p[0], box.p[3], color, 10)

        return img