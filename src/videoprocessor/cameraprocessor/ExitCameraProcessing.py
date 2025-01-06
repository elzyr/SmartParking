from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.frameprocessor.LineDetector import LineDetector


class ExitCameraProcessing:
    def __init__(self, database_connector: DatabaseConnector):
        self.database_connector = database_connector
        self.frame = None

    def run(self):
        """
            Przetwanie klatki z kamery wyjazdowej
        """

        # todo - przetwarzanie klatki z kamery wyjazdowej
        LineDetector.detect_lines(self.frame, line_color=(0, 255, 0))

        return self.frame
