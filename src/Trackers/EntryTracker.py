import cv2
import numpy as np
import skimage.filters as filters

import src.Readers.LicensePlateReader as PlateReader
from src.Signal import Signal


class EntryTracker:
    def __init__(self, addCarEntry, isCarAllowed, carAllowedToEnter: Signal, readyToCloseEntryGate: Signal):
        """
        Initializes the EntryTracker.
        Args:
            isCarAllowed - function that returns True if car is allowed to enter and False otherwise
            carAllowedToEnter - Signal that will be emmited when car that may enter is detected
            readyToCloseEntryGate - Signal that tells that the gate can be closed
        """
        self.addCarEntry = addCarEntry
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
        Verifies the car in the given image.
        Args:
            image:  The image to process.

        Returns: True if the car is verified, False otherwise.

        """
        LicensePlateReader = PlateReader.LicensePlateReader(self.isCarAllowed)
        plate_number = LicensePlateReader.read_plate(image)
        if plate_number is not None:
            self.plate_number = plate_number
            return True
        return False

    def track(self, video: str) -> bool:
        """
        Tracks the entrance of a car in the given video.
        Args:
            video: The path to the video file.

        Returns: True if the tracking was successful, False otherwise.

        """
        cap = cv2.VideoCapture(video)

        if not cap.isOpened():
            print("Error: Unable to open video.")
            return False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

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
                    continue

            if self.verifyCar(frame):
                if not self.gateOpened:
                    print("Car detected.")
                    self.openGate(self.plate_number)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Tracking finished.")
        self.closeGate()

        return True

    def getCarPositionBox(self, image: np.ndarray):
        """
        Gets the position of a car in the given image.
        Args:
            image: The image to process.

        Returns: None
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

            output = image.copy()
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            self.car_positions = []
            self.plate_number = None
            self.car_position_box = None

    def recordCarPosition(self, x, y, w, h):
        """
        Records the position of a car.
        Args:
            x: The x-coordinate of the top-left corner of the car bounding box.
            y: The y-coordinate of the top-left corner of the car bounding box.
            w: The width of the car bounding box.
            h: The height of the car bounding box.

        Returns: None
        """
        position = {"X": x, "Y": y, "Width": w, "Height": h}
        self.car_positions.append(position)
        print(f"Recorded car position: {position}")

    def openGate(self):
        """
        Opens the gate for a car. Adds an entry record to the database.

        Returns: None

        """
        self.carAllowedToEnter.emit()
        self.gateOpened = True
        self.addCarEntry(self.plate_number)

    def closeGate(self):
        """
        Closes the gate.

        Returns: None
        """
        self.readyToCloseEntryGate.emit()
        self.gateOpened = False
        print("Gate closed.")
