import MySQLdb
import unittest
from pathlib import Path

from src.DataBaseController import DataBaseController

class TestDataBaseController(unittest.TestCase):
    """
    Test suite for the DataBaseController class.
    Each test restores the database to its initial state before execution.
    """

    @staticmethod
    def reset_database():
        connection = MySQLdb.connect(host="127.0.0.1", user="root", password="", database="cyber_parking_db_test")
        cursor = connection.cursor()
        
        with open(Path(__file__).parent / "initial_db_state.sql", "r") as f:
            sql = f.read()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            for statement in sql.split(";"):
                if statement.strip():
                    cursor.execute(statement)
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

        connection.commit()
        cursor.close()
        connection.close()

    def setUp(self):
        self.reset_database()
        params = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "",
            "database": "cyber_parking_db_test"
        }
        self.db_controller = DataBaseController(params)
        connection = MySQLdb.connect(host="127.0.0.1", user="root", password="", database="cyber_parking_db_test")
        cursor = connection.cursor()
        
        cursor.execute("SELECT car_plate_id, plate_number FROM car_plates")
        result = cursor.fetchall()
        self.cars = dict(result)

        cursor.close()
        connection.close()

    def test_getIDFromPlateNumber(self):
        for car_plate_id, plate_number in self.cars.items():
            result = self.db_controller.getIDFromPlateNumber(plate_number)
            self.assertEqual(result, car_plate_id, f"Failed to get ID for plate number {plate_number}. Should be: {car_plate_id}, is: {result}")
        result = self.db_controller.getIDFromPlateNumber("NOTEXIST")
        self.assertIsNone(result, f"getIDFromPlateNumber for nonexistent plate, should retrun None, retrurned: {result}")


    def test_is_car_allowed(self):
        for plate_number in self.cars.values():
            result = self.db_controller.isCarAllowed(plate_number)
            self.assertEqual(result, True, "Expected car with plate %s to be allowed." % plate_number)

        result = self.db_controller.isCarAllowed("NONEXIST")
        self.assertEqual(result, False, "Expected car with plate 'NONEXIST' to not be allowed.")

    def test_add_car_entry(self):
        for car_plate_id, plate_number in self.cars.items():
            result = self.db_controller.addCarEntry(plate_number)
            self.assertTrue(result, f"Failed to add entry for car with ID {car_plate_id} and plate number {plate_number}")

        connection = MySQLdb.connect(**self.db_controller.params)
        cursor = connection.cursor()

        for car_plate_id in self.cars.keys():
            cursor.execute("SELECT * FROM car_movements WHERE car_plate_id = %s", (car_plate_id,))
            self.assertEqual(cursor.rowcount, 1, f"Expected 1 entry for car with ID {car_plate_id}, found {cursor.rowcount}.")

        cursor.close()
        connection.close()

    def test_add_car_exit(self):
        for car_plate_id, plate_number in self.cars.items():
            self.db_controller.addCarEntry(plate_number)
            result = self.db_controller.addCarExit(plate_number)
            self.assertTrue(result, f"Failed to add exit for car with ID {car_plate_id}., plate number: {plate_number}")

        connection = MySQLdb.connect(**self.db_controller.params)
        cursor = connection.cursor()
        for car_plate_id in self.cars.keys():
            cursor.execute("SELECT exit_time FROM car_movements WHERE car_plate_id = %s", (car_plate_id,))
            exit_time = cursor.fetchone()[0]
            self.assertIsNotNone(exit_time, f"Exit time for car with ID {car_plate_id} was not recorded.")

        cursor.close()
        connection.close()


    def test_car_took_spot(self):
        for car_plate_id, plate_number in self.cars.items():
            spot = car_plate_id
            result = self.db_controller.carTookSpot(plate_number, spot)
            self.assertTrue(result, f"Failed to record car with ID {car_plate_id} taking spot {spot}.")

        connection = MySQLdb.connect(**self.db_controller.params)
        cursor = connection.cursor()

        for car_plate_id in self.cars.keys():
            spot = car_plate_id
            cursor.execute("SELECT car_plate_id, is_free FROM parking_spaces WHERE parking_space_id = %s", (spot,))
            spot_data = cursor.fetchone()
            self.assertEqual(spot_data[0], car_plate_id, f"Expected car with ID {car_plate_id} to be in spot {spot}, found {spot_data[0]}.")
            self.assertEqual(spot_data[1], 0, f"Expected spot {spot} to be marked as not free, found free status {spot_data[1]}.")

        cursor.close()
        connection.close()

    def test_car_freed_spot(self):
        car_plate_id = 5
        spot = 1
        for car_plate_id, plate_number in self.cars.items():
            spot = car_plate_id
            result = self.db_controller.carTookSpot(plate_number, spot)
            self.assertTrue(result, f"Failed to record car with ID {car_plate_id} taking spot {spot}.")
            result = self.db_controller.carFreedSpot(spot)
            self.assertTrue(result, f"Failed to record freeing of spot {spot}.")

        connection = MySQLdb.connect(**self.db_controller.params)
        cursor = connection.cursor()
        for car_plate_id in self.cars.keys():
            spot = car_plate_id
            cursor.execute("SELECT car_plate_id, is_free FROM parking_spaces WHERE parking_space_id = %s", (spot,))
            spot_data = cursor.fetchone()
            self.assertIsNone(spot_data[0], f"Expected spot {spot} to be empty, found car ID {spot_data[0]}.")
            self.assertEqual(spot_data[1], 1, f"Expected spot {spot} to be marked as not free, found free status {spot_data[1]}.")

        cursor.close()
        connection.close()

if __name__ == "__main__":
    unittest.main()
