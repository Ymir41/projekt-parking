import cv2
import configparser
from pathlib import Path

from ParkBot import ParkBot
from DataBaseController import DataBaseController
from Trackers.EntryTracker import EntryTracker
from Trackers.ExitTracker import ExitTracker
from Trackers.CarTracker import CarTracker
from Readers.LicensePlateReader import LicensePlateReader


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent / 'config.ini')

    db_params = {
        'host': config["mysql"]["host"],
        'user': config["mysql"]["user"],
        'passwd': config["mysql"]["passwd"],
        'db': config["mysql"]["db"]
    }

    path = Path(__file__).parent.parent / 'full-video.mp4'
    cam = cv2.VideoCapture(str(path))

    if not cam.isOpened():
        print(f"Error: Could not open video {path}")
        exit(1)

    dbController = DataBaseController(db_params)

    spots_path = Path(__file__).parent.parent / 'spot-config.json'

    parkBot = ParkBot(cam, str(spots_path))
    parkBot.setCheckCar(dbController.isCarAllowed)
    parkBot.carParked.addSlot(dbController.carTookSpot)
    parkBot.carUnparked.addSlot(dbController.carFreedSpot)
    parkBot.carEntered.addSlot(dbController.addCarEntry)
    parkBot.carExited.addSlot(dbController.addCarExit)

    parkBot()

    LicensePlateReader = LicensePlateReader(parkBot.checkCar)

    entryTracker = EntryTracker(LicensePlateReader, parkBot.carEntered)

    exitTracker = ExitTracker(LicensePlateReader, parkBot.carExited)

    CarTracker = CarTracker(parkBot.cars)

    parkBot.process_video(entryTracker, exitTracker, CarTracker)

    cam.release()
    cv2.destroyAllWindows()
