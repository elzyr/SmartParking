import cv2
import numpy as np
from .ColorRange import COLOR_RANGES
from functools import reduce
from src.database.connector.DatabaseConnector import DatabaseConnector
import logging
from src.database.repository.CarRepository import CarRepository
import time


class CarDetector:
    def __init__(self, db_connector: DatabaseConnector):
        self.kernel_erode = np.ones((5, 5), np.uint8)
        self.kernel_close = np.ones((7, 7), np.uint8)
        self.color_ranges = COLOR_RANGES
        self.previous_objects = []
        self.db_connector = db_connector
        self.detected_collisions = set()
        self.car_repository = CarRepository(db_connector)
        self.collided_bounding_boxes = []
        self.colision_display_time = 0

    def detect_cars_by_color(self, hsv_image):
        """
        Tworzy maskę binarną na podstawie zakresów kolorów.
        """
        masks = [
            cv2.inRange(hsv_image, np.array(color.lower, dtype=np.uint8), np.array(color.upper, dtype=np.uint8))
            for color in self.color_ranges
        ]
        combined_mask = reduce(cv2.bitwise_or, masks)

        return combined_mask

    def mask_edges(self, frame, border_size):
        """
        Zamienia krawędzie obrazu na czarne.
        """
        frame[:border_size - 2, :] = 0
        frame[-border_size + 2:, :] = 0
        frame[:, :border_size - 5] = 0
        frame[:, -border_size + 5:] = 0
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
        h, s, v = cv2.split(hsv_image)
        v = cv2.add(v, np.full_like(v, 30))
        v = np.clip(v, 0, 255)
        hsv = cv2.merge((h, s, v))
        mask = self.detect_cars_by_color(hsv)
        mask[:15, :] = 0  # Usunięcie góry ramki
        mask[-5:, :] = 0  # Usunięcie dolu ramki
        mask[:, -5:] = 0  # Usunięcie prawej krawędzi ramki
        closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel_close)
        eroded_mask = cv2.erode(closed_mask, self.kernel_erode, iterations=1)
        cropped_mask = eroded_mask
        detected_objects = self.get_detected_objects(cropped_frame, cropped_mask)
        self.detect_collision(detected_objects, cropped_frame)
        self.previous_objects = detected_objects

        self.draw_car_localisation(cropped_frame, cropped_mask)

        frame[y1:y2, x1:x2] = cropped_frame
        self.display_colision_text(frame)
        return frame, eroded_mask

    def draw_car_localisation(self, frame, binary_mask, default_color=(150, 0, 0)):
        """
        Rysuje otoczki wypukłe wokół obiektów, które znajdują się w określonym prostokącie.
        :param frame: Obraz wejściowy (kolorowy).
        :param binary_mask: Maska binarna z wykrytymi obiektami.
        :param color: Kolor otoczki (domyślnie zielony).
        """

        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        collision_color = (215, 3, 252)  # Kolor kolizji
        # Otoczka wypukła
        for contour in contours:
            if cv2.contourArea(contour) >= 1000:
                hull = cv2.convexHull(contour)
                x, y, w, h = cv2.boundingRect(hull)
                # Zmiana koloru otoczki w przypadku kolizji
                color = default_color
                for cb in self.collided_bounding_boxes:
                    cx, cy, cw, ch = cb
                    if (x < cx + cw and cx < x + w) and (y < cy + ch and cy < y + h):
                        color = collision_color
                        break
                cv2.drawContours(frame, [hull], -1, color, 2)

    def get_detected_objects(self, frame, binary_mask):
        """
        Wykrywa obiekty na podstawie maski binarnej.
        :param frame: Obraz wejściowy.
        :param binary_mask: Maska binarna z wykrytymi obiektami.
        :return: Lista wykrytych obiektów (słowniki z obszarem i bounding box).
        """
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_objects = []

        for contour in contours:
            # Otoczka wypukła
            hull = cv2.convexHull(contour)
            area = cv2.contourArea(hull)  # Powierzchnia otoczki wypukłej
            if area >= 900:
                x, y, w, h = cv2.boundingRect(hull)
                detected_objects.append({
                    "area": area,
                    "bounding_box": (x, y, w, h)
                })
        return detected_objects

    def get_dominant_color(self, roi):
        """
        Określa dominujący kolor w regionie obiektu (ROI)
        """
        try:
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            for color_range in self.color_ranges:
                mask = cv2.inRange(
                    hsv_roi,
                    np.array(color_range.lower, dtype=np.uint8),
                    np.array(color_range.upper, dtype=np.uint8)
                )
                if cv2.countNonZero(mask) > 0:
                    return color_range.name
            return "unknown"
        except Exception as e:
            logging.error(f"Error determining dominant color: {e}")
            return "error"

    def display_colision_text(self, frame):
        if self.colision_display_time > 0:
            self.colision_display_time -= 1
            height, width, _ = frame.shape
            text_size = cv2.getTextSize(f"Collision", cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
            text_x = (width - text_size[0]) // 2
            text_y = (height - text_size[1])
            # Display the detected plate number in the center of the frame
            cv2.putText(frame, f"Collision", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)
            return frame

    def detect_collision(self, current_objects, frame):
        """
        Wykrywa zmiany w powierzchni obiektów i loguje incydent do bazy danych.
        """
        collision_pair = ()
        for current in current_objects:
            for previous in self.previous_objects:
                x1, y1, w1, h1 = current["bounding_box"]
                x2, y2, w2, h2 = previous["bounding_box"]

                overlap_x = (x1 < x2 + w2) and (x2 < x1 + w1)
                overlap_y = (y1 < y2 + h2) and (y2 < y1 + h1)
                if overlap_x and overlap_y:
                    if abs(current["area"]) > abs(previous['area']) + 2000:
                        color1 = self.get_dominant_color(frame[y1:y1 + h1, x1:x1 + w1])
                        color2 = self.get_dominant_color(frame[y2:y2 + h2, x2:x2 + w2])

                        if color2 == color1:
                            collision_pair = tuple(sorted((color1, color2)))
                            continue

                        if self.db_connector.connection is None:
                            logging.error("Brak połączenia z bazą danych - CarDetector!")
                            return

                        if collision_pair in self.detected_collisions:
                            continue
                        print(
                            f"Kolizja wykryta! {color1} {color2} Zmieniona powierzchnia: {previous['area']} -> {current['area']}")
                        self.colision_display_time = 60
                        self.car_repository.car_incidents(color1, color2, "Collision detected")
                        self.detected_collisions.add(collision_pair)

                        self.collided_bounding_boxes.append((x1, y1, w1, h1))
                        return
