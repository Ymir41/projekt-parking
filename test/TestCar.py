import unittest

from src.Trackables.Car import Car, Box

class TestCar(unittest.TestCase):

    def test_initialization(self):
        plate = "ABC123"
        box = Box.from2Corners(20, 20, 150, 150)
        
        car = Car(plate, box)

        self.assertEqual(car.label, plate)
        self.assertEqual(car.getBox(), box)


    def test_str(self):
        plate = "ABC123"
        box = Box(0, 0, 100, 0, 0, 100, 100, 100)

        spot = Car(plate, box)
        self.assertEqual("Car(\"ABC123\", Box(0, 0, 100, 0, 0, 100, 100, 100))", spot.__str__())

if __name__ == "__main__":
    unittest.main()
