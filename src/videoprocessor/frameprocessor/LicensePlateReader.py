from database.connector.DatabaseConnector import DatabaseConnector

import easyocr
import cv2
import re
import numpy as np

from database.repository.CarRepository import CarRepository


class LicensePlateReader:
    def __init__(self, database_connector: CarRepository, frame_skip=20):
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.frame_skip = frame_skip
        self.frame_count = 0
        self.database_connector = database_connector


    def check_plate(self, frame):
        self.frame_count += 1
        if self.frame_count % self.frame_skip != 0:
            return None

        copy_frame = LicensePlateReader.trim_frame(frame.copy())
        results = self.reader.readtext(copy_frame)

        for result in results:
            plate_number = result[1].replace(" ", "").upper()
            print(f"Detected text: {plate_number}")
            if LicensePlateReader.is_plate_number(plate_number):
                if self.database_connector.check_plate_in_database(plate_number):
                    print(f"Found plate: {plate_number}")
                    return plate_number

        return None

    @staticmethod
    def is_plate_number(number):
        pattern = r'^[A-Za-z]{2,3} ?[0-9]{4,5}[A-Za-z]{0,1}$'
        return bool(re.match(pattern, number, re.IGNORECASE))

    @staticmethod
    def trim_frame(copy_frame):
        height, width = copy_frame.shape[:2]
        copy_frame = copy_frame[150:(height // 2) + 150, 30:width - 30]
        gray_frame = cv2.cvtColor(copy_frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    @staticmethod
    def trim_for_color_detection(frame):
        height, width = frame.shape[:2]
        margin_y, margin_x = 50, 75
        offset_y = 100

        return frame[offset_y:offset_y + margin_y,
               300:450]

    @staticmethod
    def get_dominant_color(frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pixels = frame_rgb.reshape((-1, 3))

        mean_color = np.mean(pixels, axis=0)
        return tuple(mean_color.astype(int))
