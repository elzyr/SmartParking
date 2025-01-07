from videoprocessor.frameprocessor.GateManager import GateManager


class AllCamerasResources:
    """
        Klasa przechowująca wszystkie zasoby wspóldzielone przez kamery
    """

    def __init__(self):
        self.gate_manager = GateManager()
