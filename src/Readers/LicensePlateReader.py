import cv2
import easyocr
import numpy as np
from skimage import filters, morphology


class LicensePlateReader:
    def __init__(self, isCarAllowed):
        self.reader = easyocr.Reader(lang_list=['en'])
        self.isCarAllowed = isCarAllowed

    def plate_read_check(self, uint8_cropped_image: np.ndarray) -> tuple:
        """
        Reads the plate number and checks if the car is allowed to pass through.
        Args:
            uint8_cropped_image: The cropped image of the license plate.

        Returns: The plate number, the result of the OCR and True if the car is allowed to enter,  plate_number, res, False otherwise If could not read then 0, [], False.
        """
        res = self.reader.readtext(uint8_cropped_image, paragraph=True,
                                   allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        if len(res) == 0:
            return 0, res, False

        plate_number = res[0][1]
        plate_number = str(plate_number).replace(" ", "")
        plate_number = plate_number.upper()

        if plate_number == "":
            return 0, res, False

        if self.isCarAllowed(plate_number):
            print("Car with plate number", plate_number, "is allowed to pass through.")
            return plate_number, res, True

        print("Car with plate number", plate_number, "is not allowed. Deep inspection in progress.")
        return plate_number, res, False

    def read_plate(self, image: np.ndarray):
        """
        Reads the plate number from the given image.
        Args:
            image: The image to process.

        Returns: The car plate number if the car is allowed to enter, None otherwise.
        """
        if image is None:
            raise FileNotFoundError("Image not found.")

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        plate_number, res, is_allowed = self.plate_read_check(image_gray)
        if plate_number != 0 and is_allowed:
            return plate_number

        if len(res) == 0:
            return None

        (tl, tr, br, bl) = res[0][0]
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        cropped_image = image_gray[tl[1]:bl[1], tl[0]:tr[0]]

        thresh = cv2.threshold(cropped_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        threshed_cropped = cropped_image > thresh
        threshed_cropped = np.invert(threshed_cropped)

        uint8_cropped_image = np.uint8(threshed_cropped * 255)
        plate_number, res, is_allowed = self.plate_read_check(uint8_cropped_image)
        if plate_number != 0 and is_allowed:
            return plate_number

        triangle_thresh = filters.threshold_otsu(cropped_image)
        threshed_cropped = cropped_image > triangle_thresh

        uint8_cropped_image = np.uint8(threshed_cropped * 255)
        plate_number, res, is_allowed = self.plate_read_check(uint8_cropped_image)
        if plate_number != 0 and is_allowed:
            return plate_number

        cropped_binary_dilation = morphology.binary_dilation(threshed_cropped, morphology.disk(1))

        cropped_binary_dilation = np.uint8(cropped_binary_dilation * 255)
        plate_number, res, is_allowed = self.plate_read_check(cropped_binary_dilation)
        if plate_number != 0 and is_allowed:
            return plate_number

        li_tresh = filters.threshold_li(cropped_image)
        cropped_image_threshed = cropped_image > li_tresh

        uint8_cropped_image = np.uint8(cropped_image_threshed * 255)
        plate_number, res, is_allowed = self.plate_read_check(uint8_cropped_image)
        if plate_number != 0 and is_allowed:
            return plate_number

        cropped_image = np.uint8(cropped_image * 255)
        plate_number, res, is_allowed = self.plate_read_check(cropped_image)
        if plate_number != 0 and is_allowed:
            return plate_number

        adaptive_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 11, 2)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

        plate_number, res, is_allowed = self.plate_read_check(morph)
        if plate_number != 0 and is_allowed:
            return plate_number

        return None
