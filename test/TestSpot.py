import unittest

from src.Trackables.Spot import Spot, Box

class TestSpot(unittest.TestCase):

    def test_initialization(self):
        number = 1
        box = Box.from2Corners(0, 0, 100, 100)
        
        spot = Spot(number, box)

        self.assertEqual(spot.label, number)
        self.assertEqual(spot.getBox(), box)

    def test_str(self):
        number = 1
        box = Box(0, 0, 100, 0, 0, 100, 100, 100)

        spot = Spot(number, box)
        self.assertEqual("Spot(1, Box(0, 0, 100, 0, 0, 100, 100, 100))", spot.__str__())


if __name__ == "__main__":
    unittest.main()
