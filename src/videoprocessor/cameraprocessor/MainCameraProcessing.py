from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.cameraprocessor import AllCamerasResources
from videoprocessor.frameprocessor.LineDetector import LineDetector
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

    def run(self):
        """
            Przetwanie klatki z kamery głównej
        """

        self.car_detector.process_frame(self.frame)
        LineDetector.detect_lines(self.frame, line_color=(0, 0, 255))

        self.gate_manager.check_and_draw_gate(self.frame, camera_type=CameraType.MAIN_CAMERA.value)
        return self.frame
