import cv2
import configparser
import MySQLdb
from pathlib import Path

from ParkBot import ParkBot
from DataBaseController import DataBaseController
from Trackers.EntryTracker import EntryTracker
from Trackers.ExitTracker import ExitTracker
from Trackers.CarTracker import CarTracker
from threading import Thread, Event
from VideoViewer import VideoViewer

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
        print("Error: Could not open video.")
        exit()

    dbController = DataBaseController(db_params)

    parkBot = ParkBot(cam)
    parkBot.setCheckCar(dbController.isCarAllowed)
    parkBot.carParked.addSlot(dbController.carTookSpot)
    parkBot.carUnparked.addSlot(dbController.carFreedSpot)
    parkBot.carEntered.addSlot(dbController.addCarEntry)
    parkBot.carExited.addSlot(dbController.addCarExit)

    parkBot()

    entryTracker = EntryTracker(parkBot.carEntered, dbController.isCarAllowed,
                                parkBot.carAllowedToEnter, parkBot.readyToCloseEntryGate)

    exitTracker = ExitTracker(parkBot.carExited, dbController.isCarAllowed,
                              parkBot.carAllowedToExit, parkBot.readyToCloseExitGate)

    CarTracker = CarTracker(parkBot.cars)

    VideoViewer = VideoViewer("Parking Video")

    VideoViewer.process_video(entryTracker, exitTracker, CarTracker, str(path))
