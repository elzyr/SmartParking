from database.connector import DatabaseConnector
from database.repository.CarRepository import CarRepository
from videoprocessor.frameprocessor.GateManager import GateManager

class AllCamerasResources:
    """
        Klasa przechowująca wszystkie zasoby wspóldzielone przez kamery
    """

    def __init__(self, video_parameters, database_connector: DatabaseConnector):
        self.video_parameters = video_parameters
        self.database_connector = database_connector
        self.car_repository = CarRepository(database_connector)
        self.gate_manager = GateManager(self.video_parameters, self.car_repository)

        self.parking_spaces = self.video_parameters['parking_spaces']
