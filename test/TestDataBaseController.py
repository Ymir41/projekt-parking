import unittest
from unittest.mock import patch, MagicMock
import MySQLdb
import sys
import os

# Dodaj folder "src" do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 
from DataBaseController import DataBaseController


class TestDataBaseController(unittest.TestCase):

    def setUp(self):
        """Set up test parameters and mock the database connection."""
        self.db_params = {"host": "127.0.0.1", "user": "root", "passwd": "", "db": "test_db"}
        self.db_controller = DataBaseController(self.db_params)

    @patch("MySQLdb.connect")
    def test_is_car_allowed_valid_plate(self, mock_connect):
        """Test if the system allows a valid car plate."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, 'E0PARK')]

        allowed = self.db_controller.isCarAllowed("E0PARK")
        self.assertTrue(allowed)
        mock_cursor.execute.assert_called_once_with(
            "SELECT car_plate_id FROM car_plates WHERE plate_number = %s", ("E0PARK",)
        )

    @patch("MySQLdb.connect")
    def test_is_car_allowed_invalid_plate(self, mock_connect):
        """Test if the system denies a non-existent car plate."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = []

        allowed = self.db_controller.isCarAllowed("INVALID")
        self.assertFalse(allowed)
        mock_cursor.execute.assert_called_once_with(
            "SELECT car_plate_id FROM car_plates WHERE plate_number = %s", ("INVALID",)
        )

    @patch("MySQLdb.connect")
    def test_add_car_entry_success(self, mock_connect):
        """Test adding a car entry successfully."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        self.db_controller.addCarEntry("E0PARK")
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO car_movements (car_plate_id, entry_time) "
            "VALUES ((SELECT car_plate_id FROM car_plates WHERE plate_number = %s), NOW())", 
            ("E0PARK",)
        )
        mock_db.commit.assert_called_once()

    @patch("MySQLdb.connect")
    def test_add_car_exit_success(self, mock_connect):
        """Test adding a car exit successfully."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        self.db_controller.addCarExit("E0PARK")
        mock_cursor.execute.assert_called_once_with(
            "UPDATE car_movements SET exit_time = NOW() "
            "WHERE car_plate_id = (SELECT car_plate_id FROM car_plates WHERE plate_number = %s) "
            "AND exit_time IS NULL", 
            ("E0PARK",)
        )
        mock_db.commit.assert_called_once()

    @patch("MySQLdb.connect")
    def test_car_took_spot_success(self, mock_connect):
        """Test assigning a parking spot to a car."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        self.db_controller.carTookSpot("E0PARK", 1)
        mock_cursor.execute.assert_called_once_with(
            "UPDATE parking_spaces SET car_plate_id = (SELECT car_plate_id FROM car_plates WHERE plate_number = %s), "
            "is_free = 0 WHERE parking_space_id = %s AND is_free = 1",
            ("E0PARK", 1)
        )
        mock_db.commit.assert_called_once()

    @patch("MySQLdb.connect")
    def test_car_freed_spot_success(self, mock_connect):
        """Test freeing a parking spot."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        self.db_controller.carFreedSpot("E0PARK", 1)
        mock_cursor.execute.assert_called_once_with(
            "UPDATE parking_spaces SET car_plate_id = NULL, is_free = 1 "
            "WHERE parking_space_id = %s AND car_plate_id = (SELECT car_plate_id FROM car_plates WHERE plate_number = %s)",
            (1, "E0PARK")
        )
        mock_db.commit.assert_called_once()

    @patch("MySQLdb.connect")
    def test_edge_case_nonexistent_plate(self, mock_connect):
        """Test edge case where car plate does not exist."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.execute.side_effect = MySQLdb.Error("Car plate does not exist")
        with self.assertRaises(MySQLdb.Error):
            self.db_controller.addCarEntry("NONEXISTENT")

    @patch("MySQLdb.connect")
    def test_edge_case_duplicate_spot_assignment(self, mock_connect):
        """Test edge case of assigning a spot already taken."""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.execute.return_value = 0  # Simulate no rows updated
        self.db_controller.carTookSpot("E0PARK", 1)
        mock_cursor.execute.assert_called_once_with(
            "UPDATE parking_spaces SET car_plate_id = (SELECT car_plate_id FROM car_plates WHERE plate_number = %s), "
            "is_free = 0 WHERE parking_space_id = %s AND is_free = 1",
            ("E0PARK", 1)
        )


if __name__ == "__main__":
    unittest.main()
