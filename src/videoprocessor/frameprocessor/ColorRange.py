import numpy as np

class ColorRange:
    """Reprezentacja zakresu kolorów HSV."""
    def __init__(self, name, lower, upper):
        self.name = name
        self.lower = np.array(lower, dtype=np.uint8)
        self.upper = np.array(upper, dtype=np.uint8)

# Zakresy kolorów
COLOR_RANGES = [
        ColorRange("red1", [0, 50, 50], [10, 255, 255]),
        ColorRange("red2", [170, 50, 50], [240, 255, 255]),
        ColorRange("blue", [90, 40, 40], [150, 255, 255]),
        ColorRange("green", [50, 35, 40], [85, 255, 255]),
        ColorRange("yellow", [20, 80, 50], [50, 255, 255]),
        ColorRange("light_blue", [85, 20, 50], [190, 255, 255]),
        ColorRange("brown", [10, 20, 60], [50, 100, 200]),
]