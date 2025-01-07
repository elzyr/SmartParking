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

    def process_frames(self, frames):
        """
            Przetwarzanie klatek
            CameraType.ENTRY_CAMERA.value - kamera wjazdowa
            CameraType.MAIN_CAMERA.value - kamera główna
            CameraType.EXIT_CAMERA.value - kamera wyjazdowa
        """
        processed = []

        entry_camera_processing = EntryCameraProcessing(self.database_connector,self.all_cameras_resources)
        main_camera_processing = MainCameraProcessing(self.database_connector,self.all_cameras_resources)
        exit_camera_processing = ExitCameraProcessing(self.database_connector,self.all_cameras_resources)

        camera_type = 0
        for frame in frames:
            if frame is not None:
                """Kamera wjazdowa"""
                if camera_type == CameraType.ENTRY_CAMERA.value:
                    entry_camera_processing.frame = frame.copy()
                    processed_frame = entry_camera_processing.run()
                    processed.append(processed_frame)
                """Kamera główna"""
                if camera_type == CameraType.MAIN_CAMERA.value:
                    main_camera_processing.frame = frame.copy()
                    processed_frame = main_camera_processing.run()
                    processed.append(processed_frame)
                """Kamera wyjazdowa"""
                if camera_type == CameraType.EXIT_CAMERA.value:
                    exit_camera_processing.frame = frame.copy()
                    processed_frame = exit_camera_processing.run()
                    processed.append(processed_frame)
            else:
                processed.append(None)
            camera_type += 1
        return processed
