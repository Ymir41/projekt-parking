from Signal import Signal
import cv2
import numpy as np
from Trackers.CarTracker import CarTracker
from Trackers.SpotTracker import SpotTracker
from Trackables.Cars import Cars
from Trackables.Spots import Spots
from src.VideoViewer import draw_boxes_from_cars, VideoViewer
from src.Trackables.Cars import Box


class ParkBot(object):
    """
    A Class that monitors all relevant changes on the parking
    and announces them through Signals.
    """

    def __init__(self, cap: cv2.VideoCapture, spotConfigName: str) -> None:
        """
        :param cap: a cv2.VideoCapture video of parking
        """
        self.cap = cap
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.checkCar = None
        self.carParked = Signal()  # plate:str, spot: int
        self.carUnparked = Signal()  # place:str, spot: int
        self.carAllowedToEnter = Signal()  # plate:str
        self.carAllowedToExit = Signal()  # plate:str
        self.readyToCloseEntryGate = Signal()  # plate:str
        self.readyToCloseExitGate = Signal()  # plate:str
        self.carEntered = Signal()  # plate:str
        self.carExited = Signal()  # plate:str
        self.imageRead = Signal()  # img:np.ndarray
        self.imageTracked = Signal()  # trackedImg:np.ndarray

        self.cars = Cars((self.height, self.width))
        self.spots = Spots()
        self.carTracker = CarTracker(self.cars)
        self.spotTracker = SpotTracker(self.spots)
        self.spotTracker.loadSpots(spotConfigName)
        self.parkingState = {}  # contains parkingSpot:carPlate
        self.videoViewer = VideoViewer("Parking Video")
        self.spots_dict = {i: 0 for i in range(1, 16)}

        self.car_dict = {}

    def setCheckCar(self, func) -> None:
        """
        Sets the function used to determine whether car of given plate is allowed in.
        :param func: a function used to determine whether car of given plate number is allowed in.
        """
        self.checkCar = func

    def __call__(self):
        pass

    def parkingDiffSpots(self, oldParkingState, newParkingState) -> dict:
        ""
        out = {}
        for i in range(1, 16):
            if oldParkingState[i] != newParkingState[i]:
                out[i] = newParkingState[i]

        return out

    def getEntryAndExitFrameForOCR(self, frame: np.ndarray) -> tuple:
        """
        Crops the entry and exit frames from the given frame.
        :param frame: frame to crop entry and exit frames from.
        :return: tuple of entry_frame and exit_frame.
        """

        ocr_entry_image = frame.copy()
        ocr_exit_image = frame.copy()

        ocr_entry_image = cv2.rotate(ocr_entry_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        ocr_exit_image = cv2.rotate(ocr_exit_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        height = ocr_entry_image.shape[0]
        width = ocr_entry_image.shape[1]

        ocr_entrance_top = int(height / 1.2)
        ocr_entrance_bottom = int(height)
        ocr_entrance_left = int(width / 1.9)
        ocr_entrance_right = int(width / 1.3155)

        ocr_exit_top = int(height / 1.4)
        ocr_exit_bottom = int(height / 1.1)
        ocr_exit_left = int(width / 3.635)
        ocr_exit_right = int(width / 2.2)

        ocr_entrance = ocr_entry_image[ocr_entrance_top:ocr_entrance_bottom, ocr_entrance_left:ocr_entrance_right]
        ocr_exit = ocr_exit_image[ocr_exit_top:ocr_exit_bottom, ocr_exit_left:ocr_exit_right]

        ocr_entrance = cv2.rotate(ocr_entrance, cv2.ROTATE_180)

        return ocr_entrance, ocr_exit

    def getEntryAndExitBox(self, frame: np.ndarray) -> tuple:
        """
        Gets the entry and exit boxes from the given frame.

        :param frame: frame to get entry and exit boxes frome.
        """

        entry_image = frame.copy()

        entry_image = cv2.rotate(entry_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        height = entry_image.shape[0]
        width = entry_image.shape[1]

        top = int(height / 1.2)
        bottom = height
        left = int(width / 1.9)
        right = int(width / 1.3155)

        entry_box = Box(height - bottom, right, height - top, left, height - bottom, left, height - top, right)

        top = int(height / 1.4)
        bottom = int(height / 1.1)
        left = int(width / 3.635)
        right = int(width / 2.2)

        exit_box = Box(height - top, left, height - bottom, right, height - bottom, left, height - top, right)

        return entry_box, exit_box

    def process_video(self, entryTracker, exitTracker, carTracker) -> None:
        """
        Processes a video file entry_frame-by-entry_frame.

        :param entryTracker: EntryTracker object.
        :param exitTracker: ExitTracker object.
        :param carTracker: CarTracker object.

        """

        plates = []

        new_dims = (1000, 675)
        dim = (self.width, self.height)
        self.spots.scale(new_dims, dim)
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("End of video or error reading entry_frame.")
                break

            ocr_entrance, ocr_exit = self.getEntryAndExitFrameForOCR(frame)
            frame = cv2.resize(frame, new_dims)
            entry_box, exit_box = self.getEntryAndExitBox(frame)

            boxes = carTracker.predictBoxes(frame)
            cars = Cars.boxListToCars(boxes, new_dims)
            parked = self.spots.parked(cars)
            changes = self.parkingDiffSpots(self.spots_dict, parked)
            self.spots_dict = parked
            for change in changes.items():
                if change[1] == 0:
                    self.carUnparked.emit(change[0])
                else:
                    self.carParked.emit(change[0])

            colors = {p[0]: (100 * (p[1] == 0), 100 * (p[1] == 1), 100 * (p[1] == -1)) for p in parked.items()}
            frame = self.spots.draw(frame, colors)

            frame = cv2.rectangle(frame, entry_box.p[0], entry_box.p[3], (0, 255, 255), 3)
            frame = cv2.rectangle(frame, exit_box.p[0], exit_box.p[3], (255, 255, 0), 3)

            isEntryGateOpen = entryTracker.gateOpened
            isExitGateOpen = exitTracker.gateOpened

            is_car_entering = False
            is_car_exiting = False

            for i, car_box in enumerate(boxes):
                middle_x = (car_box.p[0][0] + car_box.p[1][0]) // 2
                middle_y = (car_box.p[0][1] + car_box.p[2][1]) // 2
                car_box_middle = (middle_x, middle_y)

                if entry_box.inside(car_box.p[0]) or entry_box.inside(car_box.p[1]) or entry_box.inside(
                        car_box.p[2]) or entry_box.inside(car_box.p[3]) or entry_box.inside(car_box_middle):
                    is_car_entering = True
                    print("Car inside entry box.")
                    frame = cv2.rectangle(frame, car_box.p[0], car_box.p[3], (255, 0, 0), 3)
                    ocr_entrance = entryTracker.process_frame(ocr_entrance)
                    plate = entryTracker.getPlateNumber()
                    if plate:
                        self.car_dict[plate] = car_box
                        plates.insert(0, entryTracker.getPlateNumber())
                        plates = list(dict.fromkeys(plates))

                elif exit_box.inside(car_box.p[0]) or exit_box.inside(car_box.p[1]) or exit_box.inside(
                        car_box.p[2]) or exit_box.inside(car_box.p[3]) or exit_box.inside(car_box_middle):
                    is_car_exiting = True
                    print("Car inside exit box.")
                    frame = cv2.rectangle(frame, car_box.p[0], car_box.p[3], (255, 0, 0), 3)
                    ocr_exit = exitTracker.process_frame(ocr_exit)

                    plate = exitTracker.getPlateNumber()
                    if plate and plate in self.car_dict:
                        self.car_dict.pop(plate)
                else:
                    frame = cv2.rectangle(frame, car_box.p[0], car_box.p[3], (0, 255, 0), 3)
                    if self.car_dict.get(plates[i]):
                        self.car_dict[plates[i]] = car_box

            if not is_car_entering:
                if isEntryGateOpen:
                    entryTracker.closeGate()

            if not is_car_exiting:
                if isExitGateOpen:
                    exitTracker.closeGate()

            self.videoViewer.displayFrame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
