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


# class TestDataBaseController(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Ustawienie połączenia z bazą danych
#         cls.connection = mysql.connector.connect(
#             host="127.0.0.1",
#             user="root",
#             passwd="",
#             db="cyber_parking_db_test"
#         )
#         cls.cursor = cls.connection.cursor()
# 
#     def setUp(self):
#         self.reset_database()
#         self.db_controller = DataBaseController(self.connection)
# 
#     def ensure_connection(self):
#         """Ensure that the connection to the database is active."""
#         #try:
#             #self.connection.ping()
#         #except MySQLdb.OperationalError:
#             #self.connection = MySQLdb.connect(
#                 #host="localhost",
#                 #user="test_user",
#                 #passwd="test_password",
#                 #db="cyber_parking_db_test"
#             #)
#             #self.cursor = self.connection.cursor()
#         pass
# 
#     @classmethod
#     def tearDownClass(cls):
#         if cls.connection:
#             try:
#                 cls.connection.close()
#             except:
#                 pass
# 
# 
#     def reset_database(self):
#         # Czyszczenie tabel
#         self.ensure_connection()
#         self.cursor.execute("DELETE FROM car_movements")
#         self.cursor.execute("UPDATE parking_spaces SET car_plate_id = NULL, is_free = 1")
# 
#         # Przywracanie danych w car_plates
#         self.cursor.execute("DELETE FROM car_plates")
#         self.cursor.execute("""
#             INSERT INTO car_plates (car_plate_id, plate_number) VALUES
#             (1, 'WE600SC'),
#             (2, 'EZG2AC5'),
#             (3, 'EPI05142'),
#             (4, 'EPIMS25'),
#             (5, 'E0PARK')
#         """)
#         self.connection.commit()
# 
#     def test_isCarAllowed_existing_plate(self):
#         self.ensure_connection()
#         # Test: Sprawdzenie, czy istniejąca tablica jest dozwolona
#         result = self.db_controller.isCarAllowed("E0PARK")
#         self.assertTrue(result)
# 
#     def test_isCarAllowed_non_existing_plate(self):
#         self.ensure_connection()
#         # Test: Sprawdzenie, czy nieistniejąca tablica jest odrzucana
#         result = self.db_controller.isCarAllowed("UNKNOWN")
#         self.assertFalse(result)
# 
#     def test_addCarEntry_new_entry(self):
#         self.ensure_connection()
#         # Test: Dodanie nowego wpisu o wjeździe
#         self.db_controller.addCarEntry("E0PARK")
#         self.cursor.execute("""
#             SELECT * FROM car_movements
#             WHERE car_plate_id = (SELECT car_plate_id FROM car_plates WHERE plate_number = 'E0PARK') 
#             AND exit_time IS NULL
#         """)
#         entry = self.cursor.fetchone()
#         self.assertIsNotNone(entry)
# 
#     def test_addCarExit_no_entry(self):
#         self.ensure_connection()
#         # Test: Próba wyjazdu bez wcześniejszego wjazdu
#         with self.assertRaises(mysql.connector.Error):
#             self.db_controller.addCarExit("E0PARK")
# 
#     def test_carTookSpot(self):
#         self.ensure_connection()
#         # Test: Przypisanie samochodu do miejsca parkingowego
#         self.db_controller.carTookSpot("E0PARK", 1)
#         self.cursor.execute("""
#             SELECT car_plate_id FROM parking_spaces
#             WHERE parking_space_id = 1 AND car_plate_id = (SELECT car_plate_id FROM car_plates WHERE plate_number = 'E0PARK')
#         """)
#         result = self.cursor.fetchone()
#         self.assertIsNotNone(result)
# 
#     def test_carFreedSpot(self):
#         self.ensure_connection()
#         # Test: Zwolnienie miejsca parkingowego
#         # Najpierw przypisz miejsce
#         self.db_controller.carTookSpot("E0PARK", 1)
#         # Teraz zwolnij miejsce
#         self.db_controller.carFreedSpot("E0PARK", 1)
#         self.cursor.execute("""
#             SELECT car_plate_id FROM parking_spaces
#             WHERE parking_space_id = 1 AND is_free = 1
#         """)
#         result = self.cursor.fetchone()
#         self.assertIsNotNone(result)
# 
#     def test_parking_space_already_taken(self):
#         self.ensure_connection()
#         # Test: Próba zajęcia już zajętego miejsca
#         self.db_controller.carTookSpot("E0PARK", 1)
#         with self.assertRaises(mysql.connector.Error):
#             self.db_controller.carTookSpot("EPI05142", 1)
# 
#     def test_car_exits_parking(self):
#         self.ensure_connection()
#         # Test: Wjazd i wyjazd samochodu
#         self.db_controller.addCarEntry("E0PARK")
#         self.db_controller.addCarExit("E0PARK")
#         self.cursor.execute("""
#             SELECT * FROM car_movements
#             WHERE car_plate_id = (SELECT car_plate_id FROM car_plates WHERE plate_number = 'E0PARK') 
#             AND exit_time IS NOT NULL
#         """)
#         result = self.cursor.fetchone()
#         self.assertIsNotNone(result)
# 
if __name__ == "__main__":
    unittest.main()
