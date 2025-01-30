import os

import numpy as np
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

from src.Trackables.Cars import Cars, Box
from src.Trackers.Tracker import Tracker

load_dotenv()


class CarTracker(Tracker):
    """
    Locates cars in an image and tracks them around the parking.
    """

    def __init__(self, cars: Cars) -> None:
        """
        :param cars: Cars object that holds the cars on the parking with their positions and boxes around them.
        """
        self.plate_number = None
        self.cars = cars
        self.CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=os.getenv("API_KEY")
        )
        self.license_plates = []
        self.license_plates_dict = {}

    def predictBoxes(self, img: np.ndarray) -> list[Box]:
        result = self.CLIENT.infer(img, model_id="hotwheels-object-detection/10")

        predictions = result.get("predictions", [])

        # print(predictions)
        predicted_cars = [
            pred for pred in predictions if
            int(pred["width"]) * int(pred["height"]) >= 6000 and float(pred["confidence"]) >= 0.55 and pred[
                "class"] == "car"
        ]

        boxes = []

        for car in predicted_cars:
            x = int(car["x"])
            y = int(car["y"])
            width = int(car["width"])
            height = int(car["height"])

            x1 = x - width // 2
            y1 = y - height // 2
            x2 = x + width // 2
            y2 = y + height // 2
            x3 = x - width // 2
            y3 = y + height // 2
            x4 = x + width // 2
            y4 = y - height // 2

            boxes.append(Box(x1, y1, x2, y2, x3, y3, x4, y4))

        return boxes
