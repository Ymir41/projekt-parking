import unittest
import numpy as np
import sys
import os

# Dodaj folder "src" do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))) 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/Trackables"))) 
from Car import Car
from Cars import Cars

class TestCars(unittest.TestCase):

    def test_initialization(self):
        dims = (5, 5)
        cars = Cars(dims)
        
        self.assertEqual(len(cars.cars), 0)
        self.assertTrue(np.array_equal(cars.locations, np.full(dims, -1)))

    def test_append_car(self):
        dims = (5, 5)
        cars = Cars(dims)
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        
        cars.append(car1)
        
        self.assertEqual(len(cars.cars), 1)
        self.assertEqual(cars[0].plate, "ABC123")
        self.assertEqual(cars.locations[2, 3], 1) 

    def test_move_car(self):
        dims = (5, 5)
        cars = Cars(dims)
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        
        cars.append(car1)
        cars.moveCar(0, (4, 4))
        
        self.assertEqual(cars[0].location, (4, 4))
        self.assertEqual(cars.locations[2, 3], -1)
        self.assertEqual(cars.locations[4, 4], 1)

    def test_move_car_to_occupied_location(self):
        dims = (5, 5)
        cars = Cars(dims)
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        car2 = Car("XYZ789", (4, 4), (0, 0, 10, 10))
        
        cars.append(car1)
        cars.append(car2)
        
        with self.assertRaises(ValueError): 
            cars.moveCar(0, (4, 4))

    def test_remove_by_plate(self):
        dims = (5, 5)
        cars = Cars(dims)
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        car2 = Car("XYZ789", (4, 4), (0, 0, 10, 10))
        
        cars.append(car1)
        cars.append(car2)
        
        cars.removeByPlate("ABC123")
        
        self.assertEqual(len(cars.cars), 1)
        self.assertEqual(cars[0].plate, "XYZ789")
        self.assertEqual(cars.locations[2, 3], -1) 
        self.assertEqual(cars.locations[4, 4], 2) 

    def test_remove_nonexistent_plate(self):
        dims = (5, 5)
        cars = Cars(dims)
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        
        cars.append(car1)
        
        with self.assertRaises(ValueError): 
            cars.removeByPlate("XYZ789")

    def test_empty_cars(self):
        dims = (5, 5)
        cars = Cars(dims)
        
        self.assertFalse(bool(cars))
        self.assertEqual(len(cars.cars), 0)
        self.assertTrue(np.array_equal(cars.locations, np.full(dims, -1)))

    def test_set_item(self):
        dims = (5, 5)
        cars = Cars(dims)
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        
        cars.append(car1)
        car2 = Car("XYZ789", (1, 1), (0, 0, 10, 10))
        
        cars[0] = car2
        
        self.assertEqual(cars[0].plate, "XYZ789")
        self.assertEqual(cars.locations[2, 3], -1)
        self.assertEqual(cars.locations[1, 1], 1)

    def test_bool_method(self):
        dims = (5, 5)
        cars = Cars(dims)
        
        self.assertFalse(bool(cars))  # Powinna być False, gdy cars jest puste
        
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        cars.append(car1)
        
        self.assertTrue(bool(cars))  # Powinna być True, gdy cars zawiera elementy

    def test_iter_method(self):
        dims = (5, 5)
        cars = Cars(dims)
        
        car1 = Car("ABC123", (2, 3), (0, 0, 10, 10))
        car2 = Car("XYZ789", (4, 4), (0, 0, 10, 10))
        
        cars.append(car1)
        cars.append(car2)
        
        cars_iterator = iter(cars)
        self.assertEqual(next(cars_iterator), car1)  # Pierwszy samochód w iteratorze
        self.assertEqual(next(cars_iterator), car2)  # Drugi samochód w iteratorze
        
        with self.assertRaises(StopIteration):  # Iterator powinien się skończyć
            next(cars_iterator)

    def test_iter_with_empty_list(self):
        dims = (5, 5)
        cars = Cars(dims)
        
        cars_iterator = iter(cars)
        with self.assertRaises(StopIteration):  # Iterator od razu powinien się skończyć
            next(cars_iterator)


if __name__ == "__main__":
    unittest.main()

