import unittest
import cv2
import os
import json
from pathlib import Path

from src.Trackers.SpotTracker import SpotTracker, Spots, Spot


class TestSpotTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        """

        cls.test_folder = Path(__file__).parent / "testSpots"
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

    def test_track(self):
        """
        Test the track method for locating spots on an image and storing them in a Spots object.
        """
        test_images = [file for file in os.listdir(self.test_folder) if
                       file.startswith("spots") and file.endswith(".jpg")]

        for img_file in test_images:
            json_file = img_file.replace(".jpg", ".json")
            json_path = os.path.join(self.test_folder, json_file)
            img_path = os.path.join(self.test_folder, img_file)

            if not os.path.exists(json_path):
                continue  # Skip if JSON file is missing

            with open(json_path, "r") as f:
                expected_data = json.load(f)

            img = cv2.imread(img_path)
            spots = Spots()
            spot_tracker = SpotTracker(spots)

            spot_tracker.track(img)

            # Assert number of spots
            self.assertEqual(len(spots), expected_data["number"], f"Failed for image: {img_file}")

            # Assert individual spot data
            for key, val in expected_data.items():
                if key == "number":
                    continue
                number = int(key.replace("box", ""))
                expected_box = tuple(val)
                spot = spots[number]
                self.assertIsNotNone(spot, f"Spot number {number} not found in image: {img_file}")
                actual_box = spot.getBox()
                tolerance = 5 # in percent
                self.assertTrue(
                    self.boxes_match(tuple(expected_box), actual_box, tolerance=(tolerance/100)),
                    f"Box mismatch for spot {number} in image: {img_file}. "
                    f"Expected: {expected_box} +/- {tolerance}%, Actual: {actual_box}"
                )

    def test_getSpotNumber(self):
        """
        Test the getSpotNumber method to ensure correct spot numbers are read from images.
        """
        spot_images = [file for file in os.listdir(self.test_folder) if
                       file.startswith("spot") and file.endswith(".jpg")]

        for img_file in spot_images:
            img_path = os.path.join(self.test_folder, img_file)
            expected_number = int(img_file.replace("spot", "").replace(".jpg", ""))

            img = cv2.imread(img_path)
            spot_tracker = SpotTracker(Spots())

            result_number = spot_tracker.getSpotNumber(img)
            self.assertEqual(result_number, expected_number, f"Spot number mismatch for image: {img_file} (should be: {expected_number}, is: {result_number}")


if __name__ == "__main__":
    unittest.main()
