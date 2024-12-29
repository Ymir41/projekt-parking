import unittest

from src.Trackables.Trackable import Trackable, Box

class TestTrackable(unittest.TestCase):
    
    def test_initialization(self):
        box = Box.from2Corners(0, 0, 100, 100)
        trackable = Trackable(None, box)
        
        self.assertEqual(trackable.getBox(), box)

if __name__ == "__main__":
    unittest.main()
