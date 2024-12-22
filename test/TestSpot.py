import unittest

from src.Trackables.Spot import Spot

class TestSpot(unittest.TestCase):

    def test_initialization(self):
        number = 1
        box = (0, 0, 100, 100)
        
        spot = Spot(number, box)

        self.assertEqual(spot.number, number)
        self.assertEqual(spot.getBox(), box)


if __name__ == "__main__":
    unittest.main()
