import cv2

from videoprocessor.videomanager.CameraType import CameraType


class GateManager:
    """
        Klasa odpowiedzialna za zarządzanie bramami wjazdowymi i wyjazdowymi
    """

    def __init__(self):
        self.__entry_gate_state = False
        self.__exit_gate_state = False
        self.__main_gate_state = False
        self.counter = 0  # dla demonstracji gate_managera

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

    def __check_entry_gate(self):
        # todo - implementacja logiki
        # przykład
        # inna_klasa = InnaKlasa()
        # if inna_klasa.warunek():
        #     self.__gate_entry_open()

        self.counter += 1  # dla demonstracji gate_managera
        if self.counter > 200:
            self.__gate_entry_open()
        if self.counter > 500:
            self.__gate_entry_close()

    def __check_exit_gate(self):
        # todo - implementacja logiki
        if self.counter > 600:
            self.__gate_exit_open()
        if self.counter > 800:
            self.__gate_exit_close()

    def check_and_draw_gate(self, frame, camera_type: CameraType):
        """
            metoda sprawdza stan i rysuje bramę
            :param frame: klatka wideo
            :param camera_type: typ kamery
        """
        if camera_type == CameraType.ENTRY_CAMERA.value:
            """Kamera wjazdowa"""
            self.__check_entry_gate()
            self.__draw_entry_gate(frame)
        elif camera_type == CameraType.MAIN_CAMERA.value:
            """Kamera główna"""
            self.__check_entry_gate()
            self.__check_exit_gate()
            self.__draw_main_gate(frame)
        elif camera_type == CameraType.EXIT_CAMERA.value:
            """Kamera końcowa"""
            self.__check_exit_gate()
            self.__draw_exit_gate(frame)

    def __draw_entry_gate(self, frame):
        """
            Rysowanie bramy wjazdowej
        """
        height, width, _ = frame.shape
        line_y = 150
        start_point = (60, line_y)
        end_point = (width - 100, line_y)
        color = (0, 0, 255)
        thickness = 10
        if self.__entry_gate_state:
            cv2.line(frame, start_point, (width - 100, line_y - 500), (0, 255, 0), thickness)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)

    def __draw_exit_gate(self, frame):
        """
            Rysowanie bramy wyjazdowej
        """
        height, width, _ = frame.shape
        line_y = 170
        start_point = (140, line_y)
        end_point = (width - 50, line_y)
        thickness = 10
        color = (0, 0, 255)
        if self.__exit_gate_state:
            cv2.line(frame, (width - 50, line_y), (140, line_y - 500), (0, 255, 0), thickness)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)

    def __draw_main_gate(self, frame):
        """Linia wjazdowa"""
        height, width, _ = frame.shape
        line_y_entry = 370
        start_point = (140, line_y_entry)
        end_point = (140, line_y_entry - 70)
        color = (0, 0, 255)
        thickness = 10
        if self.__entry_gate_state:
            cv2.line(frame, start_point, (120, line_y_entry - 70), (0, 255, 0), 5)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)

        """Linia wyjazdowa"""
        line_y_exit = 0
        start_point = (140, line_y_exit)
        end_point = (140, line_y_exit + 70)
        if self.__exit_gate_state:
            cv2.line(frame, start_point, (120, line_y_exit + 70), (0, 255, 0), 5)
        else:
            cv2.line(frame, start_point, end_point, color, thickness)
