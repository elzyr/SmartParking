import easyocr
import cv2
import re


class LicensePlateReader:
    def __init__(self, frame_skip=20):
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.frame_skip = frame_skip  # Set frame skip interval
        self.frame_count = 0  # Counter for processed frames

    def check_plate(self, frame):
        self.frame_count += 1
        if self.frame_count % self.frame_skip != 0:
            return None

        copy_frame = LicensePlateReader.trim_frame(frame.copy())
        results = self.reader.readtext(copy_frame)

        for result in results:
            plate_number = result[1]
            print(plate_number)
            if LicensePlateReader.is_plate_number(plate_number):
                print(f"Found plate: {plate_number}")
                return plate_number

        return None


    @staticmethod
    def is_plate_number(number):
        pattern = r'^[A-Za-z]{2,2} ?[0-9]{4,5}[A-Za-z]{0,1}$'
        return bool(re.match(pattern, number, re.IGNORECASE))

    @staticmethod
    def trim_frame(copy_frame):
        height, width = copy_frame.shape[:2]
        copy_frame = copy_frame[150:(height // 2) + 150, 30:width - 30]
        gray_frame = cv2.cvtColor(copy_frame, cv2.COLOR_BGR2GRAY)
        return gray_frame