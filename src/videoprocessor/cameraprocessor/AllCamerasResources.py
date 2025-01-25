from videoprocessor.frameprocessor.GateManager import GateManager
from videoprocessor.frameprocessor.LicensePlateReader import LicensePlateReader


class AllCamerasResources:
    """
        Klasa przechowująca wszystkie zasoby wspóldzielone przez kamery
    """

    def __init__(self, video_parameters):
        self.video_parameters = video_parameters
        self.license_plate_reader = LicensePlateReader()
        self.gate_manager = GateManager(self.license_plate_reader)

        self.parking_spaces = self.video_parameters['parking_spaces']
