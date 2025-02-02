from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.cameraprocessor import AllCamerasResources
from videoprocessor.videomanager.CameraType import CameraType


class EntryCameraProcessing:
    def __init__(self, database_connector: DatabaseConnector, all_cameras_resources: AllCamerasResources):
        self.database_connector = database_connector
        self.frame = None
        self.all_cameras_resources = all_cameras_resources
        self.gate_manager = all_cameras_resources.gate_manager
        self.counter = 0
        print("Init")

    def run(self):
        """
            Przetwanie klatki z kamery wjazdowej
        """

        # todo - przetwarzanie klatki z kamery wjazdowej


        # check_and_draw_gate musi byc na koncu
        self.gate_manager.check_and_draw_gate(self.frame, camera_type=CameraType.ENTRY_CAMERA.value)

        return self.frame
