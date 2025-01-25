import numpy as np
import src.Readers.LicensePlateReader as PlateReader
from src.Signal import Signal


class EntryTracker:
    """
    A class used to track the entrance of the parking lot.
    """

    def __init__(self, plate_reader: PlateReader, carEntered: Signal):
        """
        Initializes the EntryTracker.

        :param plate_reader: a LicensePlateReader used to read the plate number of the car.
        :param carEntered: a function emitted when the car enters the parking.

        """
        self.plate_reader = plate_reader
        self.carEntered = carEntered
        self.gateOpened = False
        self.car_positions = []
        self.plate_number = None

    def verifyCar(self, image: np.ndarray):
        print("ENTRY TRACKER")
        """
        Verify if the car is allowed to enter.

        :param image: The entry_frame to process.

        :return: True if the car is allowed to enter, False otherwise.

        """
        plate_number = self.plate_reader.read_plate(image)
        if plate_number is not None:
            self.plate_number = plate_number
            return True
        return False

    def process_frame(self, entry_frame: np.ndarray):
        """
        Process the exit_frame and check if the car is allowed to enter.

        :param entry_frame: The exit_frame to process.

        :return: The exit_frame with the car position box drawn if the car is detected.
        """

        if self.verifyCar(entry_frame):
            if not self.gateOpened:
                print("Car detected.")
                self.openGate()

        return entry_frame

    def openGate(self):
        """
        Open the gate for the car to enter.
        """
        self.gateOpened = True

    def closeGate(self):
        """
        Close the gate after the car has entered.
        """
        self.gateOpened = False
        self.carEntered.emit(self.plate_number)
        self.plate_number = None
        print("Entry gate closed")

    def getPlateNumber(self):
        return self.plate_number
