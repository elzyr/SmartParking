class Car:
    def __init__(self, registration, color):
        self.registration = registration
        self.color = color

    def __str__(self):
        return f"Car(registration='{self.registration}', color='{self.color}')"
