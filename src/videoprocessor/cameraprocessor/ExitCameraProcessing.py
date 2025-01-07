from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.cameraprocessor import AllCamerasResources
from videoprocessor.frameprocessor.LineDetector import LineDetector
from videoprocessor.videomanager.CameraType import CameraType


class ExitCameraProcessing:
    def __init__(self, database_connector: DatabaseConnector, all_cameras_resources: AllCamerasResources):
        self.database_connector = database_connector
        self.frame = None
        self.all_cameras_resources = all_cameras_resources
        self.gate_manager = all_cameras_resources.gate_manager

    def run(self):
        """
            Przetwanie klatki z kamery wyjazdowej
        """

        # todo - przetwarzanie klatki z kamery wyjazdowej
        LineDetector.detect_lines(self.frame, line_color=(0, 255, 0))

        # check_and_draw_gate musi byc na koncu
        self.gate_manager.check_and_draw_gate(self.frame, camera_type=CameraType.EXIT_CAMERA.value)
        return self.frame
