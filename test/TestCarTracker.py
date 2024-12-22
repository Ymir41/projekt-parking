import unittest
import cv2
import os
import json
from pathlib import Path

from src.Trackers.CarTracker import CarTracker, Cars, Car


class TestCarTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        """
        cls.test_folder = "testCars"
        cls.test_folder = Path(__file__).parent / "testCars"
        if not os.path.exists(cls.test_folder):
            raise FileNotFoundError(f"Test folder '{cls.test_folder}' not found.")

    @staticmethod
    def boxes_match(expected_box, actual_box, tolerance=0.1):
        """
        Check if two boxes match within a given tolerance.
        :param expected_box: tuple (x1, y1, x2, y2) - the expected box.
        :param actual_box: tuple (x1, y1, x2, y2) - the actual box.
        :param tolerance: float - allowed error margin as a fraction of the box size.
        :return: bool - True if the boxes match within the tolerance, False otherwise.
        """
        for i in range(4):
            size = expected_box[i % 2 + 2] - expected_box[i % 2]  # Size in x or y dimension
            error_margin = abs(size * tolerance)
            if not (expected_box[i] - error_margin <= actual_box[i] <= expected_box[i] + error_margin):
                return False
        return True

    def test_locateCars(self):
        """
        Test the locateCars method to ensure it identifies cars and their boxes correctly.
        """
        test_images = [file for file in os.listdir(self.test_folder) if
                       file.startswith("cars") and file.endswith(".jpg")]

        for img_file in test_images:
            json_file = img_file.replace(".jpg", ".json")
            json_path = os.path.join(self.test_folder, json_file)
            img_path = os.path.join(self.test_folder, img_file)

            if not os.path.exists(json_path):
                continue  # Skip if JSON file is missing

            with open(json_path, "r") as f:
                expected_data = json.load(f)

            img = cv2.imread(img_path)
            cars = Cars((img.shape[1], img.shape[0]))  # Create Cars object with image dimensions
            car_tracker = CarTracker(cars)

            located_cars = car_tracker.locateCars(img)

            # Assert number of cars
            self.assertEqual(len(located_cars), expected_data["number"], f"Failed for image: {img_file}. Should find {expected_data['number']} of cars, found {len(located_cars)} of them.")

            # Assert individual car data with tolerance
            for key, val in expected_data.items():
                if key == "number":
                    continue
                expected_box = tuple(val)
                plate = key
                expected_car = Car(plate, expected_box)
                car = located_cars.getCarOfLocation(*expected_car.getLocation())
                self.assertIsNotNone(car, f"Car with plate number {plate} (expected box: {expected_box}) not found in image: {img_file}. "
                                          f"The problem is NOT lacking or wrong plate. It's just about the box.")
                actual_box = car.getBox()
                tolerance = 5
                self.assertTrue(
                    self.boxes_match(tuple(expected_box), actual_box, tolerance=(tolerance/100)),
                    f"Box mismatch for car of plate {plate} in image: {img_file}. "
                    f"Expected: {expected_box} +/- {tolerance}%, Actual: {actual_box}"
                )
                self.assertTrue(
                    car.plate is None or car.plate == plate,
                    f"Car of plate {plate} has plate {car.plate}."
                    f"Should be None or {plate}"
                )


if __name__ == "__main__":
    unittest.main()
