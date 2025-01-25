from src.database.connector.DatabaseConnector import DatabaseConnector
import logging

from src.database.repository.CarRepository import CarRepository
from src.database.model.Car import Car
from src.videoprocessor.VideoProcessor import VideoProcessor
from video_configuration_json import video_configuration_json
from videoprocessor.frameprocessor.LicensePlateReader import LicensePlateReader


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

    # plate = LicensePlateReader("../filmy/wjazd, parkowanie  i wyjazd poprawne/1a.mp4")
    # plate.read_license_plates()
    # database_example()

    paths = [
        "../filmy/wjazd, parkowanie  i wyjazd poprawne/1a.mp4",
        "../filmy/wjazd, parkowanie  i wyjazd poprawne/1b.mp4",
        "../filmy/wjazd, parkowanie  i wyjazd poprawne/1c.mp4"
    ]
    paths = [
        "../filmy/kolejka/1a.mp4",
        "../filmy/kolejka/1b.mp4",
        "../filmy/kolejka/1c.mp4"
    ]

    video_parameters = video_configuration_json['kolejka']['parameters']
    print(video_parameters)
    processor = VideoProcessor(paths, db_config_file='../config.ini', video_parameters=video_parameters)
    processor.run()

