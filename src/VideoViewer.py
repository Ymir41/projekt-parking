import cv2
import numpy as np

class VideoViewer(object):
    def __init__(self, name:str) -> None:
        self.name = name

    def __del__(self):
        cv2.destroyWindow(self.name)

    def displayFrame(self, frame:np.ndarray):
        cv2.imshow(self.name, frame)
