import cv2
import numpy as np


def draw_boxes_from_cars(frame: np.ndarray, cars: list) -> np.ndarray:
    """
    Draws boxes around cars on the frame.
    :param frame: frame to draw boxes on.
    :param cars: list of cars to draw boxes around.
    """
    i = 0
    for car in cars:
        box = car.getBox()

        cv2.rectangle(frame, box.p[0], box.p[3], (0, 255, 0), 7)
        label = f"{i}: {box.p}"
        cv2.putText(frame, label, box.p[0], cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 7)
        i += 1

    return frame


def draw_boxes(frame: np.ndarray, boxes: list) -> np.ndarray:
    """
    Draws boxes around cars on the frame.
    :param frame: frame to draw boxes on.
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

    def __del__(self):
        cv2.destroyWindow(self.name)

    def displayFrame(self, frame: np.ndarray) -> None:
        """
        Displays a single frame of the video.
        :param frame: new frame to be displayed
        :return:
        """
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.name, 600, 400)
        cv2.imshow(self.name, frame)

    def process_video(self, entryTracker, exitTracker, carTracker, video_path: str) -> None:
        """
        Processes a video file frame-by-frame.

        :param video_path: Path to the video file.
        :param entryTracker: EntryTracker object.
        :param exitTracker: ExitTracker object.
        :param carTracker: CarTracker object.

        """
        cam = cv2.VideoCapture(video_path)

        if not cam.isOpened():
            print(f"Error: Could not open video {video_path}")
            return

        while True:
            ret, frame = cam.read()
            if not ret:
                print("End of video or error reading frame.")
                break

            entry_image = frame.copy()
            exit_image = frame.copy()

            entry_image = entryTracker.process_frame(entry_image)
            exit_image = exitTracker.process_frame(exit_image)

            frame = frame[0:frame.shape[0], 300:frame.shape[1]]

            # cars = carTracker.locateCars(frame)

            boxes = carTracker.locateCarBoxes(frame)

            frame = draw_boxes(frame, boxes)

            frame = cv2.resize(frame, (1200, 1600))
            self.displayFrame(frame)

            cv2.waitKeyEx(0)

            cv2.namedWindow("Entry", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Entry", 600, 400)
            cv2.imshow("Entry", entry_image)

            cv2.namedWindow("Exit", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Exit", 600, 400)
            cv2.imshow("Exit", exit_image)

        cam.release()
        cv2.destroyAllWindows()
