from videoprocessor.frameprocessor.GateManager import GateManager
from videoprocessor.frameprocessor.LicensePlateReader import LicensePlateReader


class AllCamerasResources:
    """
        Klasa przechowująca wszystkie zasoby wspóldzielone przez kamery
    """

    def __init__(self):
        self.license_plate_reader = LicensePlateReader()
        self.gate_manager = GateManager(self.license_plate_reader)

