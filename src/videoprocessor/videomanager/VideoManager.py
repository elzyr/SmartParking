import logging

import cv2
import numpy as np

'''
    Klasa wspomagająca zarządzanie wideo.
    Główna klasa to VideoProcessor.
'''


class VideoManager:
    def __init__(self, video_paths, target_width=650, target_height=550, target_fps=15):
        """
        Inicjalizacja klasy zarządzania wideo.
        :param video_paths: Lista ścieżek do trzech plików wideo.
        :param target_width: Docelowa szerokość wideo.
        :param target_height: Docelowa wysokość wideo.
        :param target_fps: Docelowa liczba klatek na sekundę.
        """
        self.video_paths = video_paths
        self.target_width = target_width
        self.target_height = target_height
        self.target_fps = target_fps

        '''Wczytanie wideo'''
        self.caps = [cv2.VideoCapture(path) for path in video_paths]
        self.frames = [None, None, None]  # Kluczowe klatki
        self.frame_count = [0, 0, 0]  # Liczniki klatek
        self.running = True

        '''Logowanie informacji o oryginalnym wideo'''
        self.fps = [int(cap.get(cv2.CAP_PROP_FPS)) for cap in self.caps]
        self.original_width = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) for cap in self.caps]
        self.original_height = [int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) for cap in self.caps]
        logging.info(f'Original Videos FPS: {self.fps}')
        logging.info(f'Original Videos Width: {self.original_width}')
        logging.info(f'Original Videos Height: {self.original_height}')

    def get_all_frames_resized(self):
        """
        Odczytanie klatek z trzech strumieni wideo. Zmiana rozdzielczości i FPS.
        """
        frames = []
        for i, cap in enumerate(self.caps):
            ret, frame = cap.read()
            if ret:
                frame_resized = cv2.resize(frame, (self.target_width, self.target_height))
                frames.append(frame_resized)
                self.frame_count[i] += 1
            else:
                frames.append(None)
        return frames

    def cleanup(self):
        """
        Zwolnienie zasobów po zakończeniu przetwarzania.
        """
        for cap in self.caps:
            cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def combine_frames(original_frames, processed_frames):
        """
        Łączenie oryginalnych i przetworzonych klatek w jeden obraz.
        """
        frame_height, frame_width, _ = original_frames[0].shape

        combined_frame = np.hstack([original_frames[0], original_frames[1], original_frames[2]])
        combined_processed = np.hstack([processed_frames[0], processed_frames[1], processed_frames[2]])

        combined = np.vstack([combined_frame, combined_processed])
        return combined

    @staticmethod
    def display_frames(original_frames, processed_frames):
        """
        Wyświetlanie zarówno oryginalnych, jak i przetworzonych klatek w jednym oknie.
        """
        combined = VideoManager.combine_frames(original_frames, processed_frames)
        cv2.imshow("Combined Video Feed", combined)
