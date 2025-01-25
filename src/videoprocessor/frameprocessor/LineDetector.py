import cv2
import numpy as np


class LineDetector:
    def __init__(self):
        self.frame_counter = 0
        self.lines_mask = None
        self.check_frequency = 10

    def detect_lines(self, frame, original_frame, line_color=(0, 255, 0)):
        """
        Funkcja detekcji czarnych linii (np. na drodze) - przykład prostego przetwarzania.
        """
        if self.frame_counter % self.check_frequency == 0:
            self.lines_mask = LineDetector.find_lines(original_frame)

        self.frame_counter += 1
        if self.lines_mask is not None:
            for line in self.lines_mask:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), line_color, 1)
        return frame

    @staticmethod
    def find_lines(original_frame):
        gray_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        return cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
