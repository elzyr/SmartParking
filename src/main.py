from src.database.connector.DatabaseConnector import DatabaseConnector
import logging

from src.database.repository.CarRepository import CarRepository
from src.database.model.Car import Car
from src.videoprocessor.VideoProcessor import VideoProcessor


def database_example():
    db = DatabaseConnector(config_file='../config.ini')
    db.connect()
    car1 = Car('ELCF123', 'Red')
    car2 = Car('ELCF124', 'Blue')
    car3 = Car('ELCF125', 'Green')
    repository = CarRepository(db)
    repository.insert_car(car1)
    repository.insert_car(car2)
    repository.insert_car(car3)
    cars = repository.get_cars()
    for car in cars:
        print(car)
    repository.delete_car('ELCF123')
    repository.delete_all_cars()
    db.disconnect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # database_example()

    paths = [
        "../filmy/wjazd, parkowanie  i wyjazd poprawne/1a.mp4",
        "../filmy/wjazd, parkowanie  i wyjazd poprawne/1b.mp4",
        "../filmy/wjazd, parkowanie  i wyjazd poprawne/1c.mp4"
    ]

    processor = VideoProcessor(paths, db_config_file='../config.ini')
    processor.run()

    video_paths = ["video1.mp4", "video2.mp4", "video3.mp4"]
    # Uruchomienie przetwarzania wideo
    processor = VideoProcessor(video_paths, db_config_file='../config.ini')
    processor.run()
