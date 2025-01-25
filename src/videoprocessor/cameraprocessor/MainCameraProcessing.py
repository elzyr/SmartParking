from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.cameraprocessor import AllCamerasResources
from videoprocessor.frameprocessor.LineDetector import LineDetector
from videoprocessor.frameprocessor.ParkingSpaceDetector import ParkingSpaceDetector
from videoprocessor.videomanager.CameraType import CameraType
from videoprocessor.frameprocessor.CarDetector import CarDetector
import cv2


class MainCameraProcessing:
    def __init__(self, database_connector: DatabaseConnector, all_cameras_resources: AllCamerasResources):
        self.database_connector = database_connector
        self.frame = None
        self.all_cameras_resources = all_cameras_resources
        self.gate_manager = all_cameras_resources.gate_manager
        self.car_detector = CarDetector()
        self.line_detector = LineDetector()
        self.original_frame = None
        self.parking_spaces = [
            # --- 6 miejsc w części środkowej (2 kolumny x 3 rzędy) ---
            (200, 70, 80, 120),  # lewa kolumna, górny wiersz
            (300, 70, 80, 120),  # prawa kolumna, górny wiersz
            (200, 220, 80, 120),  # lewa kolumna, środkowy wiersz
            (300, 220, 80, 120),  # prawa kolumna, środkowy wiersz
            (200, 370, 80, 120),  # lewa kolumna, dolny wiersz
            (300, 370, 80, 120),  # prawa kolumna, dolny wiersz

            # --- 4 miejsca po prawej stronie w pionie ---
            (500, 50, 80, 120),
            (500, 200, 80, 120),
            (500, 350, 80, 120),
            (500, 500, 80, 120),
        ]

    def run(self):
        """
            Przetwanie klatki z kamery głównej
        """
        self.original_frame = self.frame.copy()

        self.car_detector.process_frame(self.frame)
        self.frame = self.line_detector.detect_lines(self.frame, self.original_frame)
        ParkingSpaceDetector.detect_and_annotate(self.frame, self.original_frame, self.parking_spaces)
        self.gate_manager.check_and_draw_gate(self.frame, camera_type=CameraType.MAIN_CAMERA.value)
        return self.frame
