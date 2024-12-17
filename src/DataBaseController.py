import datetime

import MySQLdb


class DataBaseController(object):
    """
    A controller class to manage database operations related to car parking.

    Attributes:
        connection (MySQLdb.connections.Connection): The database connection object.
    """

    def __init__(self, connection) -> None:
        """
        Initializes the DataBaseController with a database connection.

        Args:
            connection (MySQLdb.connections.Connection): The database connection object.
        """
        self.connection = connection

    def __del__(self):
        """
        Closes the database connection when the object is deleted.
        """
        self.connection.close()

    def isCarAllowed(self, plate_number: str) -> int:
        """
        Checks if a car with the given plate number is allowed to enter.

        Args:
            plate_number (str): The plate number of the car.

        Returns:
            int: The car plate ID if the car is allowed, 0 otherwise.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT car_plate_id FROM car_plates WHERE plate_number = %s", (plate_number,))
        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    def addCarEntry(self, car_plate_id: int) -> bool:
        """
        Adds an entry record for a car.

        Args:
            car_plate_id (int): The ID of the car plate.

        Returns:
            bool: True if the entry was added successfully, False otherwise.
        """
        cursor = self.connection.cursor()
        result = cursor.execute("INSERT INTO car_movements (car_plate_id, entry_time) VALUES (%s,%s)",
                                (car_plate_id, datetime.datetime.now()))

        if result == 0:
            return False

        self.connection.commit()
        return True

    def addCarExit(self, car_plate_id: int) -> bool:
        """
        Adds an exit record for a car.

        Args:
            car_plate_id (int): The ID of the car plate.

        Returns:
            bool: True if the exit was added successfully, False otherwise.
        """
        cursor = self.connection.cursor()
        result = cursor.execute("UPDATE car_movements SET exit_time = %s WHERE car_plate_id = %s AND exit_time IS NULL",
                                (datetime.datetime.now(), car_plate_id))

        if result == 0:
            return False

        self.connection.commit()
        return True

    def carTookSpot(self, car_plate_id: int, spot: int) -> bool:
        """
        Records that a car took a parking spot.

        Args:
            car_plate_id (int): The ID of the car plate.
            spot (int): The parking spot number.
        """
        cursor = self.connection.cursor()
        res = cursor.execute("UPDATE parking_spaces SET car_plate_id = %s, is_free = 0 WHERE parking_space_id = %s",
                             (car_plate_id, spot))
        if res == 0:
            return False

        self.connection.commit()
        return True

    def carFreedSpot(self, spot: int) -> bool:
        """
        Records that a car freed a parking spot.

        Args:
            spot (int): The parking spot number.
        """
        cursor = self.connection.cursor()
        res = cursor.execute("UPDATE parking_spaces SET car_plate_id = NULL, is_free = 1 WHERE parking_space_id = %s",
                             (spot,))
        if res == 0:
            return False

        self.connection.commit()
        return True
