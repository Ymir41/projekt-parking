import numpy as np
import src.Readers.LicensePlateReader as PlateReader
from src.Signal import Signal


class ExitTracker:
    """
    A class used to track the exit of the parking lot.
    """

    def __init__(self, plate_reader: PlateReader, carExited: Signal):
        """
        Initializes the ExitTracker.

        :param plate_reader: a LicensePlateReader used to read the plate number of the car.
        :param carExited: a Signal used to remove a car from the parking.

        """
        self.plate_reader = plate_reader
        self.carExited = carExited
        self.gateOpened = False
        self.plate_number = None
        self.first_frame = None

    def verifyCar(self, image: np.ndarray):
        print("EXIT TRACKER")
        """
        Verify if the car is allowed to exit.

        :param image: The entry_frame to process.

        :return: True if the car is allowed to exit, False otherwise.
        """
        plate_number = self.plate_reader.read_plate(image)
        if plate_number is not None:
            self.plate_number = plate_number
            return True
        return False

    def process_frame(self, exit_frame: np.ndarray):
        """
        Processes the entry_frame and checks if the car is allowed to exit.

        :param exit_frame: The entry_frame to process.

        :return: The entry_frame with the car position box drawn if the car is detected.
        """

        if self.verifyCar(exit_frame):
            if not self.gateOpened:
                print("Car detected.")
                self.openGate()

    def openGate(self):
        """
        Opens the exit gate.
        """
        self.gateOpened = True

    def closeGate(self):
        """
        Closes the exit gate.
        """
        self.gateOpened = False
        self.carExited.emit(self.plate_number)
        self.plate_number = None
        print("Exit gate closed")
