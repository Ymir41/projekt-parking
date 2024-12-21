import cv2
import configparser
import MySQLdb
from pathlib import Path

from ParkBot import ParkBot
from DataBaseController import DataBaseController

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent /'config.ini')
    db = MySQLdb.connect(config["mysql"])

    cam = None
    dbController = DataBaseController(db)
    parkBot = ParkBot(cam)
    parkBot.setCheckCar(dbController.isCarAllowed)
    parkBot.carParked.addSlot(dbController.carTookSpot)
    parkBot.carUnparked.addSlot(dbController.carFreedSpot)
    parkBot.carEntered.addSlot(dbController.addCarEntry)
    parkBot.carExited.addSlot(dbController.addCarExit)

    parkBot()
