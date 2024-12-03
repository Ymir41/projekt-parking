import MySQLdb

class DataBaseController(object):
    def __init__(self, conection) -> None:
        self.conection = conection

    def __del__(self):
        self.conection.close()

    def isCarAllowed(self, plate: str) -> bool:
        return True

    def addCarEntry(self, plate: str) -> None:
        pass

    def addCarExit(self, plate: str) -> None:
        pass

    def carTookSpot(self, plate: str, spot: int) -> None:
        pass

    def carFreedSpot(self, plate: str, spot: int) -> None:
        pass


