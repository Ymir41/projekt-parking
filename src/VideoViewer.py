import cv2
import numpy as np


class VideoViewer(object):
    """
    A class used to display video.
    """

    def __init__(self, name: str) -> None:
        """
        :param name: name of window.
        """
        self.name = name

    def __del__(self):
        cv2.destroyWindow(self.name)

    def displayFrame(self, frame: np.ndarray) -> None:
        """
        Displays a single frame of the video.
        :param frame: new frame to be diplayed
        :return:
        """
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.name, 600, 400)
        cv2.imshow(self.name, frame)
