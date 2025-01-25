import cv2
import numpy as np


class ParkingSpaceDetector:
    @staticmethod
    def detect_and_annotate(frame, original_image, parking_spaces, threshold=0.20):
        font = cv2.FONT_HERSHEY_SIMPLEX

        for idx, (x, y, w, h) in enumerate(parking_spaces):
            roi = original_image[y:y + h, x:x + w]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            h_channel, s_channel, v_channel = cv2.split(hsv)
            mask_colorful = (s_channel > 10) & (v_channel > 30)
            total_pixels = float(w * h)
            colorful_pixels = np.count_nonzero(mask_colorful)
            occupancy = colorful_pixels / total_pixels
            if occupancy > threshold:
                color = (0, 0, 255)  # czerwony (zajęte)
                occupancy_for_display = occupancy * 3
                if occupancy_for_display > 1.0:
                    occupancy_for_display = 1.0

            else:
                color = (0, 255, 0)  # zielony (wolne)
                occupancy_for_display = occupancy  # Bez mnożenia
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = f"{idx + 1} ({occupancy_for_display * 100:.0f}%)"
            cv2.putText(frame, text, (x, y - 5), font, 0.6, color, 2, cv2.LINE_AA)

        return frame
