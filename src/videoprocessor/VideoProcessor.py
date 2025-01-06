import logging

import cv2

from database.connector.DatabaseConnector import DatabaseConnector
from videoprocessor.videomanager.CameraProcessor import CameraProcessor
from videoprocessor.videomanager.VideoManager import VideoManager

"""
    Klasa główna odpowiedzialna za synchronizowanie, przetwarzanie i wyświetlanie wideo
"""


class VideoProcessor:
    def __init__(self, video_paths: list[str], db_config_file: str):
        self.database_connector = DatabaseConnector(db_config_file)
        self.video_manager = VideoManager(video_paths)
        self.image_processor = CameraProcessor(database_connector=self.database_connector)

    def run(self):
        """
            Uruchomienie przetwarzania wideo i wyświetlanie klatek w czasie rzeczywistym.
        """
        while self.video_manager.running:
            '''Odczytanie klatek z trzech wideo'''
            frames = self.video_manager.get_all_frames_resized()

            '''Przetwarzanie wszystkie klatek wideo'''
            processed_frames = self.image_processor.process_frames(frames)
            if any(frame is None for frame in processed_frames):
                logging.info('End of video')
                break

            '''Wyświetlanie klatek w jednym oknie'''
            VideoManager.display_frames(frames, processed_frames)

            '''Zakończenie, jeśli naciśniesz 'q' na klawiaturze'''
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.video_manager.running = False

        self.video_manager.cleanup()

