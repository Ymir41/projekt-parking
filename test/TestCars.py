import unittest

from src.Trackables.Cars import Cars, Car, Box

class TestCars(unittest.TestCase):
    def setUp(self):
        self.dims = (100, 100)

    def test_initialization(self):
        cars = Cars(self.dims)
        
        self.assertEqual(len(cars), 0)
        self.assertEqual(cars.getDimensions(), self.dims)

    def test_copy(self):
        cars = Cars(self.dims)
        plate1 = "ABC123"
        car1 = Car(plate1, Box.from2Corners(0, 0, 10, 10))
        plate2 = "XYZ789"
        car2 = Car(plate2, Box.from2Corners(11, 11, 21, 21))

        cars.append(car1)
        cars.append(car2)

        cars2 = cars.copy()
        self.assertEqual(len(cars2), 2)
        self.assertEqual(cars2.getCarOfLocation(3, 3).label, plate1)
        self.assertEqual(cars2.getCarOfLocation(12, 12).label, plate2)
        plate3 = "QWE456"
        car3 = Car(plate3, Box.from2Corners(22, 22, 32, 32))
        cars2.append(car3)
        self.assertEqual(len(cars2), 3)
        self.assertEqual(cars2.getCarOfLocation(23, 23).label, plate3)
        self.assertEqual(len(cars), 2)
        self.assertEqual(cars.getCarOfLocation(23, 23), None)

        cars2.moveCar(0, Box.from2Corners(33, 33, 43, 43))
        self.assertEqual(cars2[0].getBox(), Box.from2Corners(33, 33, 43, 43))
        self.assertEqual(cars[0].getBox(), (0,0,10,10))
        self.assertEqual(cars2.getCarOfLocation(34, 34).label, plate1)
        self.assertEqual(cars.getCarOfLocation(34, 34), None)

        cars.moveCar(1, Box.from2Corners(44, 44, 54, 54))
        self.assertEqual(cars[1].getBox(), Box.from2Corners(44, 44, 54, 54))
        self.assertEqual(cars2[1].getBox(), Box.from2Corners(11, 11, 21, 21))
        self.assertEqual(cars.getCarOfLocation(45, 45).label, plate2)
        self.assertEqual(cars2.getCarOfLocation(45, 45), None)

    def test_getIndexFromPlate(self):
        cars = Cars(self.dims)
        plate1 = "ABC123"
        car1 = Car(plate1, Box.from2Corners(0, 0, 10, 10))
        plate2 = "XYZ789"
        car2 = Car(plate2, Box.from2Corners(11, 11, 21, 21))

        cars.append(car1)
        cars.append(car2)
        self.assertEqual(cars.getIndexFromPlate(plate1), 0)
        self.assertEqual(cars.getIndexFromPlate(plate2), 1)
        with self.assertRaises(ValueError):
            cars.getIndexFromPlate("NONEXIST")

    def test_getPlateFromIndex(self):
        cars = Cars(self.dims)
        plate1 = "ABC123"
        car1 = Car(plate1, Box.from2Corners(0, 0, 10, 10))
        plate2 = "XYZ789"
        car2 = Car(plate2, Box.from2Corners(11, 11, 21, 21))

        cars.append(car1)
        cars.append(car2)
        self.assertEqual(cars.getPlateFromIndex(0), plate1)
        self.assertEqual(cars.getPlateFromIndex(1), plate2)
        with self.assertRaises(IndexError):
            cars.getPlateFromIndex(3)

    def test_append_car(self):
        cars = Cars(self.dims)
        plate = "ABC123"
        car1 = Car(plate,Box.from2Corners(0, 0, 10, 10))
        
        cars.append(car1)
        
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].label, plate)
        self.assertEqual(cars.getCarOfLocation(2, 3).label, plate)

    def test_move_car(self):
        cars = Cars(self.dims)
        plate = "ABC123"
        car1 = Car(plate,  Box.from2Corners(0, 0, 10, 10))
        
        cars.append(car1)
        cars.moveCar(0, Box.from2Corners(11, 11, 21, 21))
        
        self.assertEqual(cars[0].getBox(), Box.from2Corners(11, 11, 21, 21))
        self.assertEqual(cars.getCarOfLocation(15, 15), plate)

    def test_move_car_to_occupied_location(self):
        cars = Cars(self.dims)
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        car2 = Car("XYZ789",  Box.from2Corners(11, 11, 21, 21))
        
        cars.append(car1)
        cars.append(car2)
        
        with self.assertRaises(ValueError): 
            cars.moveCar(0, Box.from2Corners(11, 11, 21, 21) )

    def test_remove_by_plate(self):
        cars = Cars(self.dims)
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        car2 = Car("XYZ789", Box.from2Corners( 11, 11, 21, 21))
        
        cars.append(car1)
        cars.append(car2)
        
        cars.removeByPlate("ABC123")
        
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].label, "XYZ789")
        self.assertEqual(cars.getCarOfLocation(2, 2), None)
        self.assertEqual(cars.getCarOfLocation(12, 22).label, "XYZ789")

    def test_remove_nonexistent_plate(self):
        cars = Cars(self.dims)
        car1 = Car("ABC123",Box.from2Corners(0, 0, 10, 10))
        
        cars.append(car1)
        
        with self.assertRaises(ValueError): 
            cars.removeByPlate("XYZ789")

    def test_empty_cars(self):
        cars = Cars(self.dims)
        
        self.assertFalse(bool(cars))
        self.assertEqual(len(cars), 0)

    def test_bool_method(self):
        cars = Cars(self.dims)
        
        self.assertFalse(bool(cars), )  # Powinna być False, gdy cars jest puste
        
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        cars.append(car1)
        
        self.assertTrue(bool(cars))  # Powinna być True, gdy cars zawiera elementy

    def test_iter_method(self):
        cars = Cars(self.dims)
        
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        car2 = Car("XYZ789", Box.from2Corners(11, 11, 21, 21))
        
        cars.append(car1)
        cars.append(car2)
        
        cars_iterator = iter(cars)
        self.assertEqual(next(cars_iterator), car1)  # Pierwszy samochód w iteratorze
        self.assertEqual(next(cars_iterator), car2)  # Drugi samochód w iteratorze
        
        with self.assertRaises(StopIteration):  # Iterator powinien się skończyć
            next(cars_iterator)

    def test_iter_with_empty_list(self):
        cars = Cars(self.dims)
        
        cars_iterator = iter(cars)
        with self.assertRaises(StopIteration):  # Iterator od razu powinien się skończyć
            next(cars_iterator)

    def test_updateCarsPositions_with_full_plates(self):
        cars = Cars(self.dims)
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        car2 = Car("XYZ789", Box.from2Corners(11, 11, 21, 21))

        cars.append(car1)
        cars.append(car2)

        # With positions overlapping
        cars2 = Cars(self.dims)
        car1_2 = Car("ABC123", Box.from2Corners(3, 3 , 13, 13))
        car2_2 = Car("XYZ789", Box.from2Corners(14, 14, 24, 24))

        cars2.append(car1_2)
        cars2.append(car2_2)

        cars_test = cars.copy()
        cars_test.updateCarsPositions(cars2)
        self.assertEqual(cars_test["ABC123"].getBox(), Box.from2Corners(3, 3, 13, 13))
        self.assertEqual(cars_test["XYZ789"].getBox(), Box.from2Corners(14, 14, 24, 24))

        # Far away
        cars2 = Cars(self.dims)
        car1_2 = Car("ABC123", Box.from2Corners(70, 70, 80, 80))
        car2_2 = Car("XYZ789", Box.from2Corners(84, 84, 94, 94))

        cars2.append(car1_2)
        cars2.append(car2_2)

        cars_test = cars.copy()
        cars_test.updateCarsPositions(cars2)
        self.assertEqual(cars_test["ABC123"].getBox(), Box.from2Corners(70, 70, 80, 80))
        self.assertEqual(cars_test["XYZ789"].getBox(), Box.from2Corners(84, 84, 94, 94))

    def test_updateCarsPositions_with_some_plates(self):
        cars = Cars(self.dims)
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        car2 = Car("XYZ789", Box.from2Corners(11, 11, 21, 21))

        cars.append(car1)
        cars.append(car2)

        # With positions overlapping
        cars2 = Cars(self.dims)
        car1_2 = Car("ABC123", Box.from2Corners(3, 3, 13, 13))
        car2_2 = Car(None, Box.from2Corners(14, 14, 24, 24))

        cars2.append(car1_2)
        cars2.append(car2_2)

        cars_test = cars.copy()
        cars_test.updateCarsPositions(cars2)
        self.assertEqual(cars_test["ABC123"].getBox(), Box.from2Corners(3, 3, 13, 13))
        self.assertEqual(cars_test["XYZ789"].getBox(), Box.from2Corners(14, 14, 24, 24))

        # Far away
        cars2 = Cars(self.dims)
        car1_2 = Car("ABC123", Box.from2Corners(70, 70, 80, 80))
        car2_2 = Car(None, Box.from2Corners(15, 15, 25, 25))

        cars2.append(car1_2)
        cars2.append(car2_2)

        cars_test = cars.copy()
        cars_test.updateCarsPositions(cars2)
        self.assertEqual(cars_test["ABC123"].getBox(), Box.from2Corners(70, 70, 80, 80))
        self.assertEqual(cars_test["XYZ789"].getBox(), Box.from2Corners(15, 15, 25, 25))

    def test_updateCarsPositions_without_plates(self):
        cars = Cars(self.dims)
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        car2 = Car("XYZ789", Box.from2Corners(11, 11, 21, 21))

        cars.append(car1)
        cars.append(car2)

        # With positions overlapping
        cars2 = Cars(self.dims)
        car1_2 = Car(None, Box.from2Corners(3, 3, 13, 13))
        car2_2 = Car(None, Box.from2Corners(14, 14, 24, 24))

        cars2.append(car1_2)
        cars2.append(car2_2)

        cars_test = cars.copy()
        cars_test.updateCarsPositions(cars2)
        self.assertEqual(cars_test["ABC123"].getBox(), Box.from2Corners(3, 3, 13, 13))
        self.assertEqual(cars_test["XYZ789"].getBox(), Box.from2Corners(14, 14, 24, 24))

        # Further away
        cars2 = Cars(self.dims)
        car1_2 = Car(None, Box.from2Corners(8, 8, 18, 18))
        car2_2 = Car(None, Box.from2Corners(15, 15, 25, 25))

        cars2.append(car1_2)
        cars2.append(car2_2)

        cars_test = cars.copy()
        cars_test.updateCarsPositions(cars2)
        self.assertEqual(cars_test["ABC123"].getBox(), Box.from2Corners(8, 8, 18, 18))
        self.assertEqual(cars_test["XYZ789"].getBox(), Box.from2Corners(15, 15, 25, 25))

    def test_updateCarsPositions_without_plates_no_overlap(self):
        cars = Cars(self.dims)
        car1 = Car("ABC123", Box.from2Corners(0, 0, 10, 10))
        car2 = Car("XYZ789", Box.from2Corners(11, 11, 21, 21))

        cars.append(car1)
        cars.append(car2)

        # With positions overlapping
        cars2 = Cars(self.dims)
        car1_2 = Car(None, Box.from2Corners(0, 15, 10, 25))
        car2_2 = Car(None, Box.from2Corners(14, 14, 24, 24))

        cars2.append(car1_2)
        cars2.append(car2_2)

        cars_test = cars.copy()
        cars_test.updateCarsPositions(cars2)
        self.assertEqual(cars_test["ABC123"].getBox(), Box.from2Corners(0, 15, 10, 25))
        self.assertEqual(cars_test["XYZ789"].getBox(), Box.from2Corners(14, 14, 24, 24))

if __name__ == "__main__":
    unittest.main()

