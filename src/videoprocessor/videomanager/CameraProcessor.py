from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.cameraprocessor.AllCamerasResources import AllCamerasResources
from videoprocessor.videomanager.CameraType import CameraType
from videoprocessor.cameraprocessor.EntryCameraProcessing import EntryCameraProcessing
from videoprocessor.cameraprocessor.ExitCameraProcessing import ExitCameraProcessing
from videoprocessor.cameraprocessor.MainCameraProcessing import MainCameraProcessing

"""
    Klasa przetwarzająca wszystkie kamery
    Poszczególne kamery są w pakiecie cameraprocessor
"""


class CameraProcessor:

    def __init__(self, database_connector: DatabaseConnector):
        self.database_connector = database_connector
        self.all_cameras_resources= AllCamerasResources()
        self.entry_camera_processing = EntryCameraProcessing(self.database_connector,self.all_cameras_resources)
        self.main_camera_processing = MainCameraProcessing(self.database_connector,self.all_cameras_resources)
        self.exit_camera_processing = ExitCameraProcessing(self.database_connector,self.all_cameras_resources)


    def process_frames(self, frames):
        """
            Przetwarzanie klatek
            CameraType.ENTRY_CAMERA.value - kamera wjazdowa
            CameraType.MAIN_CAMERA.value - kamera główna
            CameraType.EXIT_CAMERA.value - kamera wyjazdowa
        """
        processed = []


        camera_type = 0
        for frame in frames:

            if frame is not None:
                """Kamera wjazdowa"""
                if camera_type == CameraType.ENTRY_CAMERA.value:
                    self.entry_camera_processing.frame = frame.copy()
                    processed_frame = self.entry_camera_processing.run()
                    processed.append(processed_frame)
                """Kamera główna"""
                if camera_type == CameraType.MAIN_CAMERA.value:
                    self.main_camera_processing.frame = frame.copy()
                    processed_frame = self.main_camera_processing.run()
                    processed.append(processed_frame)
                """Kamera wyjazdowa"""
                if camera_type == CameraType.EXIT_CAMERA.value:
                    self.exit_camera_processing.frame = frame.copy()
                    processed_frame = self.exit_camera_processing.run()
                    processed.append(processed_frame)
            else:
                processed.append(None)
            camera_type += 1
        return processed
