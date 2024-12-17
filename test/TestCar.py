import unittest
import sys
import os

# Dodaj folder "src" do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/Trackables"))) 
from Car import Car
from Signal import Signal

class TestCar(unittest.TestCase):

    def test_initialization(self):
        plate = "ABC123"
        location = (50, 60)
        box = (20, 20, 150, 150)
        
        car = Car(plate, location, box)

        self.assertEqual(car.plate, plate)
        self.assertEqual(car.location, location)
        self.assertEqual(car.box, box)
        self.assertIsInstance(car.moved, Signal)

    def test_inherited_move_updates_attributes(self):
        plate = "XYZ789"
        location = (100, 120)
        box = (30, 30, 160, 160)
        new_location = (150, 200)
        new_box = (40, 40, 170, 170)

        car = Car(plate, location, box)
        car.move(new_location, new_box)

        self.assertEqual(car.location, new_location)
        self.assertEqual(car.box, new_box)

    def test_inherited_moved_signal_emit(self):
        plate = "LMN456"
        location = (70, 80)
        box = (25, 25, 140, 140)
        new_location = (90, 100)
        self.signal_called = False
        self.emitted_location = None

        def on_moved(location):
            self.signal_called = True
            self.emitted_location = location

        car = Car(plate, location, box)
        car.moved.addSlot(on_moved)

        car.move(new_location, box)

        self.assertTrue(self.signal_called)
        self.assertEqual(self.emitted_location, new_location)

    def test_plate_attribute(self):
        plate = "DEF456"
        location = (10, 20)
        box = (0, 0, 100, 100)
        
        car = Car(plate, location, box)

        self.assertEqual(car.plate, "DEF456")


if __name__ == "__main__":
    unittest.main()
