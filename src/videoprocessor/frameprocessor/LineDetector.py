import cv2
import numpy as np


class LineDetector:
    @staticmethod
    def detect_lines(frame, line_color=(255, 0, 0)):
        """
        Funkcja detekcji białych linii (np. na drodze) - przykład prostego przetwarzania.
        """
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # Wykrywanie linii Hough
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), line_color, 2)
        return frame
