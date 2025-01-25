import unittest
import cv2
import os
import json
from pathlib import Path

from src.Trackers.SpotTracker import SpotTracker, Spots, Spot
from src.Trackables.Box import Box


class TestSpotTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        """

        cls.test_folder = Path(__file__).parent / "testSpots"
        if not os.path.exists(cls.test_folder):
            raise FileNotFoundError(f"Test folder '{cls.test_folder}' not found.")

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
                expected_box = Box(*val)
                spot = spots[number]
                self.assertIsNotNone(spot, f"Spot number {number} not found in image: {img_file}")
                actual_box = spot.getBox()
                tolerance = 5 # in %
                self.assertTrue(
                    Box.almostEqual(expected_box, actual_box, tolerance=(tolerance / 100)),
                    f"Box mismatch for spot {number} in image: {img_file}. "
                    f"Expected: {expected_box} +/- {tolerance}%, Actual: {actual_box}"
                )

    def test_getSpotNumber(self):
        """
        Test the getSpotNumber method to ensure correct spot numbers are read from images.
        """
        spot_images = [file for file in os.listdir(self.test_folder) if
                       file.startswith("spot") and not file.startswith("spots") and file.endswith(".jpg")]

        for img_file in spot_images:
            img_path = os.path.join(self.test_folder, img_file)
            expected_number, orientation =img_file.replace("spot", "").replace(".jpg", "").split("-")
            expected_number = int(expected_number)
            orientation = orientation.upper()

            img = cv2.imread(img_path)
            spot_tracker = SpotTracker(Spots())

            result_number = spot_tracker.getSpotNumber(img, orientation)
            self.assertEqual(result_number, expected_number, f"Spot number mismatch for image: {img_file} (should be: {expected_number}, is: {result_number}")


if __name__ == "__main__":
    unittest.main()
