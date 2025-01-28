import os
from typing import List

import cv2
import numpy as np
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

from src.Trackables.Box import Box
from src.Trackables.Cars import Cars, Car, Box
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

    def track(self, img: np.ndarray) -> None:
        """
        Updates the locations of the cars in self.cars with positions of cars found in the image.
        :param img: img with the new state of parking with cars to track.
        """
        pass

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

    def drawBoxes(self, img: np.ndarray, boxes: List[Box]) -> np.ndarray:
        """
        Draws boxes around cars on the frame.
        :param img: frame to draw boxes on.
        :param boxes: list of boxes to draw.
        :return: img with boxes drawn around cars.
        """
        for box in boxes:
            cv2.rectangle(img, box.p[0], box.p[3], (0, 255, 0), 3)

        return img

    def locateCarBoxes(self, img: np.ndarray, license_plate: str) -> Cars:
        """
        Locates cars on an image of parking and returns their boxes.
        :param img: the image with cars to locate

        :return: list[Box] - a list of boxes around cars found in the image.
        """
        result = self.CLIENT.infer(img, model_id="hotwheels-object-detection/10")

        predictions = result.get("predictions", [])

        print(predictions)
        predicted_cars = [
            pred for pred in predictions if
            int(pred["width"]) * int(pred["height"]) >= 400000 and float(pred["confidence"]) >= 0.55 and pred[
                "class"] == "car"
        ]

        # boxes = []
        cars = Cars(dimensions=(img.shape[0], img.shape[1]))

        for i, car in enumerate(predicted_cars):
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

            # if car.getBox().withinRange(box) or car.getBox().distance(box) <= car.getBox().distance(box) * tolerance:

            if license_plate is not None:
                # self.license_plates.append(license_plate)
                self.license_plates.insert(0, license_plate)
                self.license_plates = list(dict.fromkeys(self.license_plates))
                # self.license_plates_dict[self.license_plates[0]] = Box(x1, y1, x2, y2, x3, y3, x4, y4)

            # If this is the last car, append with the license plate, otherwise append with None
            # if i == len(predicted_cars) - 1:
            cars.append(Car(self.license_plates[i], Box(x1, y1, x2, y2, x3, y3, x4, y4)))
            # else:
            #     cars.append(Car(None, Box(x1, y1, x2, y2, x3, y3, x4, y4)))

        # return boxes
        return cars

    def locateCars(self, img: np.ndarray, license_plate: str, tolerance: float = 3.0) -> Cars:
        """
        Locates cars on an image of the parking, draws bounding boxes with license plates
        only for newly added cars, and returns a collection of Car objects.

        :param img: The image of the parking lot with cars to locate.
        :param license_plate: License plate for the detected car.
        :param tolerance: Tolerance factor for determining whether a car is close enough to an existing one.
        :return: Cars - a collection of Car objects found in the image.
        """
        # Find bounding boxes around cars using locateCarBoxes
        boxes = self.locateCarBoxes(img)
        detected_cars = Cars(dimensions=(img.shape[0], img.shape[1]))
        last_added_car = None  # Track the last newly added car

        print(len(boxes))

        # for box in boxes:
        #     # Check if the detected box matches an existing car
        #     existing_car = None
        #     for car in self.cars:
        #         # Match based on license plate or proximity
        #         if car.getPlate() == license_plate:
        #             existing_car = car
        #             break
        #         if car.getBox().withinRange(box) or car.getBox().distance(box) <= car.getBox().distance(
        #                 box) * tolerance:
        #             existing_car = car
        #             break
        #
        #     if existing_car:
        #         # Update the box of the existing car
        #         existing_car.move(box)
        #         print(f"Updated car: {existing_car}")
        #     else:
        #         # Add a new car
        #         new_car = Car(plate=license_plate if license_plate else None, box=box)
        #         detected_cars.append(new_car)
        #         last_added_car = new_car  # Mark this car as the last added
        #         print(f"New car added: {new_car}")
        #
        #     # Draw the box and display the license plate only for the last added car
        #     cv2.rectangle(img, box.p[0], box.p[3], (0, 255, 0), 7)
        #     if last_added_car and last_added_car.getBox() == box:
        #         # Display the license plate only for the last added car
        #         text_position = (box.p[0][0], max(box.p[0][1] - 15, 15))
        #         text_label = license_plate
        #         cv2.putText(
        #             img, text_label, text_position,
        #             cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 7, cv2.LINE_AA
        #         )
        #
        # # Update the collection of cars
        # self.cars.updateCarsPositions(detected_cars)
        #
        # return self.cars
