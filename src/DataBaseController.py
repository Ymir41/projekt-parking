import datetime

import MySQLdb


class DataBaseController(object):
    """
    A controller class to manage database operations related to car parking.

    Attributes:
        params (dict) parameters of connection
        connection (MySQLdb.connections.Connection): The database connection object.
    """

    def __init__(self, params) -> None:
        self.params = params
        self.connection = None
        self.cursor = None

    @staticmethod
    def connect(func):
        def wrapper(self, *args, **kwargs):
            to_close = False
            if self.connection == None:
                to_close = True
                db = MySQLdb.connect(**self.params)
                self.connection = db
                self.cursor = db.cursor()

            res = func(self, *args, **kwargs)

            if to_close:
                self.cursor.close()
                self.cursor = None
                self.connection = None
                db.close()
            return res

        return wrapper

    @connect
    def getIDFromPlateNumber(self, plate_number: str):
        """
        Returns car_plate_id of given plate_number, if plate_number not existant, then 0.

        Args:
            plate_number (str): The plate number of the car.

        Returns:
            int: car_plate_id, of that car if not in database, then None
        """
        self.cursor.execute("SELECT car_plate_id FROM car_plates WHERE plate_number = %s", (plate_number,))
        car_plate_id = self.cursor.fetchone()
        if car_plate_id is None:
            return None
        return car_plate_id[0]

    @connect
    def isCarAllowed(self, plate_number: str) -> bool:
        """
        Checks if a car with the given plate number is allowed to enter.

        Args:
            plate_number (str): The plate number of the car.

        Returns:
            bool: True if the car is allowed, False otherwise
        """
        self.cursor.execute("SELECT car_plate_id FROM car_plates WHERE plate_number = %s", (plate_number,))
        result = self.cursor.fetchone()

        if result is None:
            return False

        return True

    @connect
    def addCarEntry(self, plate_number: str) -> bool:
        """
        Adds an entry record for a car.

        Args:
            plate_number (str): The plate number of the car plate.

        Returns:
            bool: True if the entry was added successfully, False otherwise.
        """
        car_plate_id = self.getIDFromPlateNumber(plate_number)
        result = self.cursor.execute("INSERT INTO car_movements (car_plate_id, entry_time) VALUES (%s,%s)",
                                     (car_plate_id, datetime.datetime.now()))

        if result == 0:
            return False

        self.connection.commit()
        return True

    @connect
    def addCarExit(self, plate_number: str) -> bool:
        """
        Adds an exit record for a car.

        Args:
            plate_number (str): The plate number of the car plate.

        Returns:
            bool: True if the exit was added successfully, False otherwise.
        """
        car_plate_id = self.getIDFromPlateNumber(plate_number)
        result = self.cursor.execute(
            "UPDATE car_movements SET exit_time = %s WHERE car_plate_id = %s AND exit_time IS NULL",
            (datetime.datetime.now(), car_plate_id))

        if result == 0:
            return False

        self.connection.commit()
        return True

    @connect
    def carTookSpot(self, parking_spot_id: int) -> bool:
        """
        Records that a car took a parking spot.

        Args:
            parking_spot_id (int): The parking spot number.
        """
        res = self.cursor.execute(
            "UPDATE parking_spaces SET is_free = 0 WHERE parking_space_id = %s",
            (parking_spot_id,))

        if res == 0:
            return False

        self.connection.commit()
        return True

    @connect
    def carFreedSpot(self, parking_spot_id: int) -> bool:
        """
        Records that a car freed a parking spot.

        Args:
            parking_spot_id (int): The parking spot number.
        """
        res = self.cursor.execute(
            "UPDATE parking_spaces SET is_free = 1 WHERE parking_space_id = %s",
            (parking_spot_id,))
        if res == 0:
            return False

        self.connection.commit()
        return True
