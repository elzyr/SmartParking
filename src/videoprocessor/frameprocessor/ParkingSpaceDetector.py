import cv2
import numpy as np


class ParkingSpaceDetector:
    @staticmethod
    def detect_and_annotate(frame, original_image, parking_spaces, threshold=0.20):
        font = cv2.FONT_HERSHEY_SIMPLEX
        results = []
        # -- KROK 1: Detekcja zajętości --
        for idx, (x, y, w, h) in enumerate(parking_spaces):
            roi = original_image[y: y + h, x: x + w]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            h_channel, s_channel, v_channel = cv2.split(hsv)
            mask_colorful = (s_channel > 20) & (v_channel > 50)
            total_pixels = float(w * h)
            colorful_pixels = np.count_nonzero(mask_colorful)
            occupancy = colorful_pixels / total_pixels
            if occupancy > threshold:
                color = (0, 0, 255)  # czerwony
                occupancy_for_display = occupancy * 3
                if occupancy_for_display > 1.0:
                    occupancy_for_display = 1.0
            else:
                color = (0, 255, 0)  # zielony
                occupancy_for_display = occupancy
            results.append((idx, x, y, w, h, color, occupancy_for_display))

        # -- KROK 2: Rysowanie wyników na klatce --
        for (idx, x, y, w, h, color, occupancy_for_display) in results:
            # Prostokąt
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            # Tekst z wynikiem
            text = f"{idx + 1} ({occupancy_for_display * 100:.0f}%)"
            cv2.putText(frame, text, (x + 7, y + 23), font, 0.55, color, 2, cv2.LINE_AA)

        return frame
