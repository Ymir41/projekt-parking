import unittest

from src.Trackables.Spots import Spots, Spot
from src.Trackables.Cars import Cars, Car, Box

class TestSpots(unittest.TestCase):

    def test_append_and_size(self):
        spots = Spots()
        spot1 = Spot(1,  Box.from2Corners(0, 0, 50, 50))
        spot2 = Spot(2,  Box.from2Corners(50, 50, 100, 100))
        
        spots.append(spot1)
        spots.append(spot2)
        
        self.assertEqual(len(spots), 2)
        self.assertEqual(spots[1], spot1)
        self.assertEqual(spots[2], spot2)

    def test_getitem(self):
        spots = Spots()
        spot1 = Spot(1, Box.from2Corners(0, 0, 50, 50))
        spot2 = Spot(2,  Box.from2Corners(50, 50, 100, 100))
        
        spots.append(spot1)
        spots.append(spot2)
        
        self.assertEqual(spots[1], spot1)
        self.assertEqual(spots[2], spot2)

        with self.assertRaises(KeyError):
            spots[3].getBox()

    def test_parkedCars_with_empty_spots(self):
        spots = Spots()
        spot1 = Spot(1, Box.from2Corners(0, 0, 50, 50))
        spot2 = Spot(2,  Box.from2Corners(50, 50, 100, 100))
        cars = Cars((100, 100))
        
        spots.append(spot1)
        spots.append(spot2)
        
        parked = spots.parkedCars(cars)
        self.assertEqual(parked, {1: None, 2: None})

    def test_parkedCars_with_cars(self):
        spots = Spots()
        spot1 = Spot(1, Box.from2Corners(0, 0, 50, 50))
        spot2 = Spot(2,  Box.from2Corners(50, 50, 100, 100))
        
        car1 = Car("ABC123", Box.from2Corners(0, 0, 50, 50))
        car2 = Car("XYZ789",  Box.from2Corners(50, 50, 100, 100))

        cars = Cars((200, 200))
        cars.append(car1)
        cars.append(car2)
        
        spots.append(spot1)
        spots.append(spot2)
        
        parked = spots.parkedCars(cars)
        self.assertEqual(parked, {1: "ABC123", 2: "XYZ789"})

    def test_parkedCars_mixed(self):
        spots = Spots()
        spot1 = Spot(1, Box.from2Corners(0, 0, 50, 50))
        spot2 = Spot(2,  Box.from2Corners(50, 50, 100, 100))
        
        car1 = Car("ABC123",  Box.from2Corners(0, 0, 50, 50))
        car2 = Car("XYZ890", Box.from2Corners(52, 1, 102, 51))
        cars = Cars((200, 200))
        cars.append(car1)
        cars.append(car2)

        spots.append(spot1)
        spots.append(spot2)
        
        parked = spots.parkedCars(cars)
        self.assertEqual(parked, {1: "ABC123", 2: None})

    def test_bool_method(self):
        spots = Spots()
        
        self.assertFalse(bool(spots))  # Powinno być False, gdy spots jest pusty
        
        spot1 = Spot(1, Box.from2Corners(0, 0, 50, 50))
        spots.append(spot1)
        
        self.assertTrue(bool(spots))  # Powinno być True, gdy spots zawiera elementy

    def test_items_method(self):
        spots = Spots()
        
        spot1 = Spot(1,  Box.from2Corners(0, 0, 50, 50))
        spot2 = Spot(2,  Box.from2Corners(50, 50, 100, 100))
        
        spots.append(spot1)
        spots.append(spot2)

        i = 0
        s = [spot1, spot2]
        for num, spot in spots.items():
            self.assertEqual(num, i+1, "wrong number of spot")
            self.assertEqual(spot, s[i], "wrong spot")
            i+=1
        self.assertEqual(i, 2, f"There should be 2 items in spots.items(), found {i}")

    def test_items_with_empty_spots(self):
        spots = Spots()

        i =0
        for num, spot in spots.items():
            i+=1
        self.assertEqual(i, 0, f"There should be 0 items in empty spots.items(), found {i}")


if __name__ == "__main__":
    unittest.main()

