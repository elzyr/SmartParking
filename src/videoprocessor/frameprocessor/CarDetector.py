import cv2
import numpy as np
from .ColorRange import COLOR_RANGES

class CarDetector:
    def __init__(self):
        self.kernel_close = np.ones((4, 4), np.uint8)
        self.color_ranges = COLOR_RANGES

    def detect_cars_by_color(self, hsv_image):
        """
        Tworzy maskę binarną na podstawie zakresów kolorów.
        """
        mask_total = np.zeros(hsv_image.shape[:2], dtype=np.uint8)
        for color in self.color_ranges:
            lower_bound = np.array(color.lower, dtype=np.uint8)
            upper_bound = np.array(color.upper, dtype=np.uint8)
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
            mask_total = cv2.bitwise_or(mask_total, mask)
        return mask_total

    def mask_edges(self, frame, border_size):
        """
        Zamienia krawędzie obrazu na czarne.
        """
        mask = np.ones_like(frame, dtype=np.uint8) * 255
        mask[:border_size, :] = 0
        mask[-border_size:, :] = 0
        mask[:, :border_size] = 0
        mask[:, -border_size:] = 0
        return cv2.bitwise_and(frame, mask)

    def process_frame(self, frame):
        """
        Przetwarza obraz wejściowy:
        - Przycina obraz i maskę do wybranej ramki.
        - Wykrywa samochody (keypoints).
        - Rysuje obrysy na oryginalnym obrazie.
        """
        rect_coords = (200, 0, frame.shape[1], frame.shape[0])  # Współrzędne ramki (poczatek bramki)
        x1, y1, x2, y2 = rect_coords

        # Przycięcie obrazu do ramki
        cropped_frame = frame[y1:y2, x1:x2]

        # Tworzenie maski
        hsv_image = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        mask = self.detect_cars_by_color(hsv_image)
        mask[:15, :] = 0  # Usunięcie góry ramki
        closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel_close)
        eroded_mask = cv2.erode(closed_mask, np.ones((4, 4), np.uint8), iterations=1)

        # Przycięcie maski do ramki
        cropped_mask = eroded_mask

        # Rysowanie konturów
        self.draw_keypoints(cropped_frame, cropped_mask, rect_coords)

        # Wstawienie przetworzonego fragmentu z powrotem do obrazu
        frame[y1:y2, x1:x2] = cropped_frame

        return frame, eroded_mask

    def draw_keypoints(self, frame,binary_mask,rect_coords, color=(0, 255, 0)):
        """
        Rysuje otoczki wypukłe wokół obiektów, które znajdują się w określonym prostokącie.
        :param frame: Obraz wejściowy (kolorowy).
        :param binary_mask: Maska binarna z wykrytymi obiektami.
        :param rect_coords: Współrzędne prostokąta (x1, y1, x2, y2).
        :param color: Kolor otoczki (domyślnie zielony).
        :param min_area: Minimalna powierzchnia konturu do uwzględnienia.
        """

        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x1, y1, x2, y2 = rect_coords

        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= 800:
                # Otoczka wypukła
                hull = cv2.convexHull(contour)
                cv2.drawContours(frame, [hull], -1, color, 2)
