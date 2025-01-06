from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.frameprocessor.LineDetector import LineDetector


class MainCameraProcessing:
    def __init__(self, database_connector: DatabaseConnector):
        self.database_connector = database_connector
        self.frame = None

    def run(self):
        """
            Przetwanie klatki z kamery głównej
        """

        # todo - przetwarzanie klatki z kamery głównej
        LineDetector.detect_lines(self.frame, line_color=(0, 0, 255))

        return self.frame
