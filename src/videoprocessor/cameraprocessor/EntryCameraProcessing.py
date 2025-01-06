from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.frameprocessor.LineDetector import LineDetector


class EntryCameraProcessing:
    def __init__(self, database_connector: DatabaseConnector):
        self.database_connector = database_connector
        self.frame = None

    def run(self):
        """
            Przetwanie klatki z kamery wjazdowej
        """

        # todo - przetwarzanie klatki z kamery wjazdowej
        LineDetector.detect_lines(self.frame, line_color=(255, 0, 0))

        return self.frame
