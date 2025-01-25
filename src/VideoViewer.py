import cv2
import numpy as np


def draw_boxes_from_cars(frame: np.ndarray, cars: list) -> np.ndarray:
    """
    Draws boxes around cars on the entry_frame.
    :param frame: entry_frame to draw boxes on.
    :param cars: list of cars to draw boxes around.
    """
    i = 0
    for car in cars:
        license_plate = car.getPlate()
        box = car.getBox()

        cv2.rectangle(frame, box.p[0], box.p[3], (0, 255, 0), 7)
        text_position = (box.p[0][0], max(box.p[0][1] - 15, 15))
        text_label = license_plate
        print("License plate: ", license_plate)
        cv2.putText(
            frame, text_label, text_position,
            cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 7, cv2.LINE_AA
        )
        i += 1

    return frame


def draw_boxes(frame: np.ndarray, boxes: list) -> np.ndarray:
    """
    Draws boxes around cars on the entry_frame.
    :param frame: entry_frame to draw boxes on.
    :param boxes: list of boxes to draw.
    """
    for box in boxes:
        cv2.rectangle(frame, box.p[0], box.p[3], (0, 255, 0), 7)

    return frame


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
