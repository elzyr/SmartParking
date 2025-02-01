import threading

from database.repository.CarRepository import CarRepository
from videoprocessor.frameprocessor.LicensePlateReader import LicensePlateReader
from videoprocessor.videomanager.CameraType import CameraType
from database.connector.DatabaseConnector import DatabaseConnector

import cv2


class GateManager:
    """
        Klasa odpowiedzialna za zarządzanie bramami wjazdowymi i wyjazdowymi
    """

    def __init__(self, video_parameters, database_connector: CarRepository):
        self.__entry_gate_state = False
        self.__exit_gate_state = False
        self.__main_gate_state = False
        self.database_connector = database_connector
        self.license_plate_reader = LicensePlateReader(database_connector)
        self.license_plate_reader_exit = LicensePlateReader(database_connector)
        self.opened_entry_gate_time = 0
        self.opened_exit_gate_time = 0
        self.entry_gate_height = video_parameters['entry_gate_height']
        self.exit_gate_height = video_parameters['exit_gate_height']
        self.main_gate_entry_height = video_parameters['main_gate_entry_height']
        self.main_gate_exit_width = video_parameters['main_gate_exit_width']
        self.main_gate_distance = video_parameters['main_gate_distance']

    def __check_entry_gate(self, frame):
        plate = self.license_plate_reader.check_plate(frame)
        if plate is not None:
            print('Plate')
            self.opened_entry_gate_time = 120
            self.__entry_gate_state = True

        if self.opened_entry_gate_time > 0:
            # print('Opened')
            self.opened_entry_gate_time -= 1
        else:
            # print('Closed')
            self.__entry_gate_state = False

    def __check_exit_gate(self, frame):
        plate = self.license_plate_reader_exit.check_plate(frame)
        if plate is not None:
            self.opened_exit_gate_time = 120
            self.__exit_gate_state = True

        if self.opened_exit_gate_time > 0:
            self.opened_exit_gate_time -= 1
        else:
            self.__exit_gate_state = False

    def __process_entry_gate_in_background(self, frame):
        """Ta funkcja będzie wywoływać __check_entry_gate w tle"""
        self.__check_entry_gate(frame)

    def __process_exit_gate_in_background(self, frame):
        """Ta funkcja będzie wywoływać __check_exit_gate w tle"""
        self.__check_exit_gate(frame)

    def check_and_draw_gate(self, frame, camera_type: CameraType):
        """
            metoda sprawdza stan i rysuje bramę
            :param frame: klatka wideo
            :param camera_type: typ kamery
        """
        if camera_type == CameraType.ENTRY_CAMERA.value:
            """Kamera wjazdowa"""
            entry_thread = threading.Thread(target=self.__process_entry_gate_in_background, args=(frame,))
            entry_thread.daemon = True
            entry_thread.start()
            self.__draw_entry_gate(frame)
        elif camera_type == CameraType.MAIN_CAMERA.value:
            """Kamera główna"""
            self.__draw_main_gate(frame)
        elif camera_type == CameraType.EXIT_CAMERA.value:
            """Kamera końcowa"""
            exit_thread = threading.Thread(target=self.__process_exit_gate_in_background, args=(frame,))
            exit_thread.daemon = True
            exit_thread.start()
            self.__draw_exit_gate(frame)

    def __draw_entry_gate(self, frame):
        """
            Rysowanie bramy wjazdowej
        """
        height, width, _ = frame.shape
        start_point = (60, self.entry_gate_height)
        end_point = (width - 100, self.entry_gate_height)
        color = (0, 0, 255)
        thickness = 10
        if self.__entry_gate_state:
            cv2.line(frame, start_point, (width - 100, self.entry_gate_height - 500), (0, 255, 0), thickness)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)

    def __draw_exit_gate(self, frame):
        """
            Rysowanie bramy wyjazdowej
        """
        height, width, _ = frame.shape
        start_point = (140, self.exit_gate_height)
        end_point = (width - 50, self.exit_gate_height)
        thickness = 10
        color = (0, 0, 255)
        if self.__exit_gate_state:
            cv2.line(frame, (width - 50, self.exit_gate_height), (140, self.exit_gate_height - 500), (0, 255, 0),
                     thickness)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)

    def __draw_main_gate(self, frame):
        """Linia wjazdowa"""
        height, width, _ = frame.shape
        line_y_entry = self.main_gate_entry_height
        start_point = (self.main_gate_exit_width, line_y_entry)
        end_point = (self.main_gate_exit_width, line_y_entry - 70)
        color = (0, 0, 255)
        thickness = 10
        if self.__entry_gate_state:
            cv2.line(frame, start_point, (self.main_gate_exit_width - 20, line_y_entry - 70), (0, 255, 0), 5)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)

        """Linia wyjazdowa"""
        line_y_exit = self.main_gate_entry_height + self.main_gate_distance
        start_point = (self.main_gate_exit_width, line_y_exit)
        end_point = (self.main_gate_exit_width, line_y_exit + 70)
        if self.__exit_gate_state:
            cv2.line(frame, start_point, (self.main_gate_exit_width - 20, line_y_exit + 70), (0, 255, 0), 5)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)

    def __gate_entry_open(self):
        self.__entry_gate_state = True

    def __gate_entry_close(self):
        self.__entry_gate_state = False

    def get_entry_gate_state(self):
        return self.__entry_gate_state

    def __gate_exit_open(self):
        self.__exit_gate_state = True

    def __gate_exit_close(self):
        self.__exit_gate_state = False

    def get_exit_gate_state(self):
        return self.__exit_gate_state
