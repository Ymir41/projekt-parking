import cv2
import numpy as np
import skimage.filters as filters

import src.Readers.LicensePlateReader as PlateReader
from src.Signal import Signal


class EntryTracker:
    """
    A class used to track the entrance of the parking lot.
    """

    def __init__(self, carEntered: Signal, isCarAllowed, carAllowedToEnter: Signal, readyToCloseEntryGate: Signal):
        """
        Initializes the EntryTracker.

        :param carEntered: a function emitted when the car enters the parking.
        :param isCarAllowed: a function used to determine whether car of given plate number is allowed in.
        :param carAllowedToEnter: a Signal emitted when the car is allowed to enter.
        :param readyToCloseEntryGate: a Signal emitted when the gate is ready to close.

        """
        self.carEntered = carEntered
        self.isCarAllowed = isCarAllowed
        self.carAllowedToEnter = carAllowedToEnter
        self.readyToCloseEntryGate = readyToCloseEntryGate
        self.gateOpened = False
        self.car_position_box = None
        self.car_positions = []
        self.plate_number = None
        self.first_frame = None

    def verifyCar(self, image: np.ndarray):
        """
        Verify if the car is allowed to enter.

        :param image: The frame to process.

        :return: True if the car is allowed to enter, False otherwise.

        """
        LicensePlateReader = PlateReader.LicensePlateReader(self.isCarAllowed)
        plate_number = LicensePlateReader.read_plate(image)
        if plate_number is not None:
            self.plate_number = plate_number
            return True
        return False

    def process_frame(self, frame: np.ndarray):
        """
        Process the frame and check if the car is allowed to enter.

        :param frame: The frame to process.

        :return: The frame with the car position box drawn if the car is detected.
        """
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        height = frame.shape[0]
        width = frame.shape[1]
        frame = frame[int(height / 1.2):height, int(width / 1.9):width - 960]
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        if self.first_frame is None:
            self.first_frame = frame

        if self.gateOpened:
            self.getCarPositionBox(frame)
            if self.car_position_box is None and self.gateOpened:
                print("car passed the gate.")
                self.closeGate()
                return frame
            else:
                cv2.rectangle(frame, (self.car_position_box[0], self.car_position_box[1]),
                              (self.car_position_box[0] + self.car_position_box[2],
                               self.car_position_box[1] + self.car_position_box[3]), (0, 255, 0), 2)
                return frame

        if self.verifyCar(frame):
            if not self.gateOpened:
                print("Car detected.")
                self.openGate()

        return frame

    def getCarPositionBox(self, image: np.ndarray):
        """
        Get the position of the car in the frame.
        :param image: The frame to process.

        :return: The frame with the car position box drawn if the car is detected.
        """
        background = cv2.cvtColor(self.first_frame, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blurred_img = cv2.GaussianBlur(image_gray, (9, 9), 9)
        blurred_bg = cv2.GaussianBlur(background, (9, 9), 9)
        diff = cv2.absdiff(blurred_bg, blurred_img)

        blurred = diff

        thresh = filters.threshold_li(blurred)
        binary = blurred < thresh
        binary = np.invert(binary)
        binary = np.uint8(binary * 255)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (40, 40))
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        morph = cv2.copyMakeBorder(morph, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        edges = cv2.Canny(morph, 30, 100)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        min_area = 7500
        car_contour = None
        last_position = self.car_positions[-1] if self.car_positions else None
        min_distance = float('inf')
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if min_area < cv2.contourArea(contour):
                if last_position:
                    contour_center = (x + w // 2, y + h // 2)
                    last_center = (
                        last_position["X"] + last_position["Width"] // 2,
                        last_position["Y"] + last_position["Height"] // 2,
                    )
                    distance = ((contour_center[0] - last_center[0]) ** 2 +
                                (contour_center[1] - last_center[1]) ** 2) ** 0.5
                    if distance < min_distance and distance < 500:
                        min_distance = distance
                        car_contour = contour
                else:
                    car_contour = contour
                    break

        if car_contour is not None:
            x, y, w, h = cv2.boundingRect(car_contour)
            self.car_position_box = (x, y, w, h)
            self.recordCarPosition(x, y, w, h)

        else:
            self.car_positions = []
            self.plate_number = None
            self.car_position_box = None

    def recordCarPosition(self, x, y, w, h):
        """
        Record the position of the car.
        """
        position = {"X": x, "Y": y, "Width": w, "Height": h}
        self.car_positions.append(position)
        print(f"Recorded car position: {position}")

    def openGate(self):
        """
        Open the gate for the car to enter.
        """
        self.carAllowedToEnter.emit()
        self.gateOpened = True
        self.carEntered.emit(self.plate_number)

    def closeGate(self):
        """
        Close the gate after the car has entered.
        """
        self.readyToCloseEntryGate.emit()
        self.gateOpened = False
        print("Gate closed")

    def getPlateNumber(self):
        return self.plate_number