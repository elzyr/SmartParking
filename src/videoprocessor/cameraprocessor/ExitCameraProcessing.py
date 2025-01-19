from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.cameraprocessor import AllCamerasResources


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

        return self.frame
