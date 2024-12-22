import unittest

from src.Trackables.Car import Car

class TestCar(unittest.TestCase):

    def test_initialization(self):
        plate = "ABC123"
        box = (20, 20, 150, 150)
        
        car = Car(plate, box)

        self.assertEqual(car.plate, plate)
        self.assertEqual(car.getBox(), box)

if __name__ == "__main__":
    unittest.main()
