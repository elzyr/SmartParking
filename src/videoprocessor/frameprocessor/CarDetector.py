import cv2
import numpy as np
from .ColorRange import COLOR_RANGES
from functools import reduce

class CarDetector:
    def __init__(self):
        self.kernel_close_erode = np.ones((4, 4), np.uint8)
        self.color_ranges = COLOR_RANGES

    def detect_cars_by_color(self, hsv_image):
        """
        Tworzy maskę binarną na podstawie zakresów kolorów.
        """
        masks = [cv2.inRange(hsv_image, np.array(color.lower, dtype=np.uint8), np.array(color.upper, dtype=np.uint8))
                 for color in self.color_ranges]
        return reduce(cv2.bitwise_or, masks)

    def mask_edges(self, frame, border_size):
        """
        Zamienia krawędzie obrazu na czarne.
        """
        frame[:border_size, :] = 0
        frame[-border_size:, :] = 0
        frame[:, :border_size] = 0
        frame[:, -border_size:] = 0
        return frame

    def process_frame(self, frame):
        """
        Przetwarza obraz wejściowy:
        - Przycina obraz i maskę do wybranej ramki.
        - Rysuje obrysy na oryginalnym obrazie.
        """
        rect_coords = (200, 0, frame.shape[1], frame.shape[0])  # Współrzędne ramki (poczatek bramki)
        x1, y1, x2, y2 = rect_coords

        cropped_frame = frame[y1:y2, x1:x2]

        hsv_image = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        mask = self.detect_cars_by_color(hsv_image)
        mask[:15, :] = 0  # Usunięcie góry ramki
        closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel_close_erode)
        eroded_mask = cv2.erode(closed_mask, self.kernel_close_erode, iterations=1)
        cropped_mask = eroded_mask

        self.draw_car_localisation(cropped_frame, cropped_mask)

        frame[y1:y2, x1:x2] = cropped_frame

        return frame, eroded_mask

    def draw_car_localisation(self, frame, binary_mask, color=(0, 255, 0)):
        """
        Rysuje otoczki wypukłe wokół obiektów, które znajdują się w określonym prostokącie.
        :param frame: Obraz wejściowy (kolorowy).
        :param binary_mask: Maska binarna z wykrytymi obiektami.
        :param color: Kolor otoczki (domyślnie zielony).
        """

        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Otoczka wypukła
        filtered_contours = [cv2.convexHull(contour) for contour in contours if cv2.contourArea(contour) >= 800]
        cv2.drawContours(frame, filtered_contours, -1, color, 2)
