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

    def displayFrame(self, frame: np.ndarray) -> None:
        """
        Displays a single entry_frame of the video.
        :param frame: new entry_frame to be displayed
        :return:
        """
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.name, 1000, 675)
        cv2.imshow(self.name, frame)
