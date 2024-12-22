import unittest

from src.Trackables.Trackable import Trackable

class TestTrackable(unittest.TestCase):
    
    def test_initialization(self):
        box = (0, 0, 100, 100)
        trackable = Trackable(box)
        
        self.assertEqual(trackable.getBox(), box)

if __name__ == "__main__":
    unittest.main()
