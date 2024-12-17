import unittest
import sys
import os

# Dodaj folder "src" do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 
from Signal import Signal
from Trackables.Trackable import Trackable

class TestTrackable(unittest.TestCase):
    
    def test_initialization(self):
        location = (10, 20)
        box = (0, 0, 100, 100)
        trackable = Trackable(location, box)
        
        self.assertEqual(trackable.location, location)
        self.assertEqual(trackable.box, box)
        self.assertIsInstance(trackable.moved, Signal)

    def test_move_updates_attributes(self):
        location = (10, 20)
        box = (0, 0, 100, 100)
        new_location = (30, 40)
        new_box = (10, 10, 110, 110)
        
        trackable = Trackable(location, box)
        trackable.move(new_location, new_box)
        
        self.assertEqual(trackable.location, new_location)
        self.assertEqual(trackable.box, new_box)

    def test_moved_signal_emit(self):
        location = (10, 20)
        box = (0, 0, 100, 100)
        new_location = (30, 40)
        self.signal_called = False
        self.emitted_location = None
        
        def on_moved(location):
            self.signal_called = True
            self.emitted_location = location

        trackable = Trackable(location, box)
        trackable.moved.addSlot(on_moved)
        
        trackable.move(new_location, box)

        self.assertTrue(self.signal_called)
        self.assertEqual(self.emitted_location, new_location)

if __name__ == "__main__":
    unittest.main()
