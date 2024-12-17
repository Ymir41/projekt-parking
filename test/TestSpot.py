import unittest
import sys
import os

# Dodaj folder "src" do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/Trackables"))) 
from Spot import Spot
from Signal import Signal

class TestSpot(unittest.TestCase):

    def test_initialization(self):
        number = 1
        location = (10, 20)
        box = (0, 0, 100, 100)
        
        spot = Spot(number, location, box)

        self.assertEqual(spot.number, number)
        self.assertEqual(spot.location, location)
        self.assertEqual(spot.box, box)
        self.assertIsInstance(spot.moved, Signal)

    def test_inherited_move_updates_attributes(self):
        number = 2
        location = (15, 25)
        box = (5, 5, 105, 105)
        new_location = (30, 40)
        new_box = (10, 10, 110, 110)

        spot = Spot(number, location, box)
        spot.move(new_location, new_box)

        self.assertEqual(spot.location, new_location)
        self.assertEqual(spot.box, new_box)

    def test_inherited_moved_signal_emit(self):
        number = 3
        location = (20, 30)
        box = (10, 10, 110, 110)
        new_location = (40, 50)
        self.signal_called = False
        self.emitted_location = None

        def on_moved(location):
            self.signal_called = True
            self.emitted_location = location

        spot = Spot(number, location, box)
        spot.moved.addSlot(on_moved)

        spot.move(new_location, box)

        self.assertTrue(self.signal_called)
        self.assertEqual(self.emitted_location, new_location)

if __name__ == "__main__":
    unittest.main()
