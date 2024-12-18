import cv2
import numpy as np
import skimage.filters as filters

import src.DataBaseController as DataBaseController
import src.Readers.LicensePlateReader as PlateReader


class EntryTracker:
    def __init__(self, db: DataBaseController):
        """
        Initializes the EntryTracker.
        Args:
            db: The database controller.
        """
        self.db = db
        self.gateOpened = False
        self.car_position_box = None
        self.car_positions = []
        self.car_plate_id = None

    def verifyCar(self, image: np.ndarray):
        """
        Verifies the car in the given image.
        Args:
            image:  The image to process.

        Returns: True if the car is verified, False otherwise.

        """
        LicensePlateReader = PlateReader.LicensePlateReader(self.db)
        car_plate_id, plate_number = LicensePlateReader.read_plate(image)
        if car_plate_id != 0 and plate_number != 0:
            self.car_plate_id = car_plate_id
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

            frame = frame[int(frame.shape[0] / 1.3):frame.shape[0] - 200,
                    int(frame.shape[1] / 2) + 100:frame.shape[1] - 1100]
            frame = cv2.resize(frame, (640, 480))

            prepared_frame = cv2.rotate(frame, cv2.ROTATE_180)

            if self.gateOpened:
                self.getCarPositionBox(prepared_frame)
                if self.car_position_box is None and self.gateOpened:
                    print("here " + str(self.car_position_box))
                    self.closeGate()
                    continue

            if self.verifyCar(prepared_frame):
                if not self.gateOpened:
                    self.openGate(self.car_plate_id)

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
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 9)

        thresh = filters.threshold_li(blurred)
        binary = blurred > thresh
        binary = np.invert(binary)
        binary = np.uint8(binary * 255)
        cv2.imshow("Binary", binary)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("Morph", morph)
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
            print(f"Area: {cv2.contourArea(contour)}")
            if min_area < cv2.contourArea(contour):
                if last_position:
                    contour_center = (x + w // 2, y + h // 2)
                    last_center = (
                        last_position["X"] + last_position["Width"] // 2,
                        last_position["Y"] + last_position["Height"] // 2,
                    )
                    # Calculate distance
                    distance = ((contour_center[0] - last_center[0]) ** 2 +
                                (contour_center[1] - last_center[1]) ** 2) ** 0.5
                    print(f"Distance: {distance}")
                    if distance < min_distance and distance < 250:
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
            cv2.imshow("Detected Car", output)
            cv2.waitKey(1)
        else:
            cv2.imshow("Not Detected Car", image)
            cv2.waitKey(1)
            self.car_positions = []
            self.car_plate_id = None
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

    def openGate(self, car_plate_id: int):
        """
        Opens the gate for a car. Adds an entry record to the database.
        Args:
            car_plate_id: The ID of the car plate.

        Returns: None

        """
        if self.db.addCarEntry(car_plate_id):
            self.gateOpened = True
            print("Gate opened.")
        else:
            print("Failed to open gate.")

    def closeGate(self):
        """
        Closes the gate.

        Returns: None
        """
        self.gateOpened = False
        print("Gate closed.")
