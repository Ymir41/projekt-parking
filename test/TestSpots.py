import unittest
import sys
import os

# Dodaj folder "src" do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/Trackables"))) 
from Spot import Spot
from Car import Car
from Cars import Cars
from Spots import Spots

class TestSpots(unittest.TestCase):

    def test_append_and_size(self):
        spots = Spots()
        spot1 = Spot(1, (10, 20), (0, 0, 50, 50))
        spot2 = Spot(2, (30, 40), (50, 50, 100, 100))
        
        spots.append(spot1)
        spots.append(spot2)
        
        self.assertEqual(len(spots.spots), 2)
        self.assertIn(1, spots.spots)
        self.assertIn(2, spots.spots)

    def test_getitem(self):
        spots = Spots()
        spot1 = Spot(1, (10, 20), (0, 0, 50, 50))
        spot2 = Spot(2, (30, 40), (50, 50, 100, 100))
        
        spots.append(spot1)
        spots.append(spot2)
        
        self.assertEqual(spots[1], spot1)
        self.assertEqual(spots[2], spot2)

    def test_parkedCars_with_empty_spots(self):
        spots = Spots()
        spot1 = Spot(1, (0, 0), (0, 0, 50, 50))
        spot2 = Spot(2, (50, 50), (50, 50, 100, 100))
        cars = Cars((100, 100))
        
        spots.append(spot1)
        spots.append(spot2)
        
        parked = spots.parkedCars(cars)
        self.assertEqual(parked, {1: None, 2: None})

    def test_parkedCars_with_cars(self):
        spots = Spots()
        spot1 = Spot(1, (0, 0), (0, 0, 50, 50))
        spot2 = Spot(2, (50, 50), (50, 50, 100, 100))
        
        car1 = Car("ABC123", (10, 20), (0, 0, 50, 50))
        car2 = Car("XYZ789", (60, 60), (50, 50, 100, 100))

        cars = Cars((100,100))
        cars.append(car1)
        cars.append(car2)
        
        spots.append(spot1)
        spots.append(spot2)
        
        parked = spots.parkedCars(cars)
        self.assertEqual(parked, {1: "ABC123", 2: "XYZ789"})

    def test_parkedCars_mixed(self):
        spots = Spots()
        spot1 = Spot(1, (0, 0), (0, 0, 50, 50))
        spot2 = Spot(2, (50, 50), (50, 50, 100, 100))
        
        car1 = Car("ABC123", (10, 20), (0, 0, 50, 50))
        cars = Cars((100, 100))
        cars.append(car1)
        
        spots.append(spot1)
        spots.append(spot2)
        
        parked = spots.parkedCars(cars)
        self.assertEqual(parked, {1: "ABC123", 2: None})

    def test_bool_method(self):
        spots = Spots()
        
        self.assertFalse(bool(spots))  # Powinno być False, gdy spots jest pusty
        
        spot1 = Spot(1, (10, 20), (0, 0, 50, 50))
        spots.append(spot1)
        
        self.assertTrue(bool(spots))  # Powinno być True, gdy spots zawiera elementy

    def test_iter_method(self):
        spots = Spots()
        
        spot1 = Spot(1, (10, 20), (0, 0, 50, 50))
        spot2 = Spot(2, (30, 40), (50, 50, 100, 100))
        
        spots.append(spot1)
        spots.append(spot2)
        
        spots_iterator = iter(spots)
        
        self.assertEqual(next(spots_iterator), spot1)  # Pierwszy obiekt Spot
        self.assertEqual(next(spots_iterator), spot2)  # Drugi obiekt Spot
        
        with self.assertRaises(StopIteration):  # Iterator powinien się skończyć
            next(spots_iterator)

    def test_iter_with_empty_spots(self):
        spots = Spots()
        
        spots_iterator = iter(spots)
        with self.assertRaises(StopIteration):  # Iterator od razu powinien się skończyć
            next(spots_iterator)


if __name__ == "__main__":
    unittest.main()

