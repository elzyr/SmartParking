import cv2
import numpy as np


class ParkingSpaceDetector:
    @staticmethod
    def detect_and_annotate(frame, original_image, parking_spaces, threshold=0.7):
        """
        Metoda, która w jednej kolejce:
          1. Oblicza wypełnienie (occupancy) dla każdego miejsca parkingowego,
          2. Sprawdza, czy przekracza ono zadany threshold,
          3. Rysuje wyniki (ramki i numery) bezpośrednio na klatce (frame).

        Zwraca klatkę z naniesionymi adnotacjami.
        """
        # Ustawiamy czcionkę do rysowania tekstu.
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Przetwarzamy każde miejsce parkingowe po kolei.
        for idx, (x, y, w, h) in enumerate(parking_spaces):

            # Wycinamy fragment obrazu (ROI) dla danego miejsca.
            roi = original_image[y:y + h, x:x + w]

            # -- KROK 1: obliczenie occupancy (zajętości) --
            # Konwersja do odcieni szarości
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # Progowanie – np. wszystko poniżej 150 to "auto"
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

            # Obliczamy procent (w [0..1]) pikseli traktowanych jako 'zajęte'
            total_pixels = thresh.shape[0] * thresh.shape[1]
            black_pixels = np.count_nonzero(thresh)
            occupancy = black_pixels / total_pixels

            # -- KROK 2: sprawdzamy threshold --
            if occupancy > threshold:
                color = (0, 0, 255)  # czerwony w BGR
            else:
                color = (0, 255, 0)  # zielony w BGR

            # -- KROK 3: rysowanie ramki i numeru z % zajętości --
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = f"{idx + 1} ({occupancy * 100:.0f}%)"
            cv2.putText(frame, text, (x, y - 5), font, 0.6, color, 2, cv2.LINE_AA)

        # Zwracamy przetworzoną klatkę z adnotacjami.
        return frame
