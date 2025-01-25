from src.database.connector.DatabaseConnector import DatabaseConnector
import logging

from src.database.repository.CarRepository import CarRepository
from src.database.model.Car import Car
from src.videoprocessor.VideoProcessor import VideoProcessor
from video_configuration_json import video_configuration_json
import os


def get_specific_files_list(directory_name, video_number):
    video_number = str(video_number)
    matching_files = []
    directory_name = f'../filmy/{directory_name}'
    for filename in os.listdir(directory_name):
        if filename.startswith(video_number) and len(filename) > 2 and filename[1] in ['a', 'b',
                                                                                       'c'] and filename.endswith(
            ".mp4"):
            matching_files.append(os.path.join(directory_name, filename))

    return matching_files


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

    directory = 'wjazd, parkowanie  i wyjazd poprawne'
    paths = get_specific_files_list(directory, 1)

    video_parameters = video_configuration_json[directory]['parameters']
    print(video_parameters)
    processor = VideoProcessor(paths, db_config_file='../config.ini', video_parameters=video_parameters)
    processor.run()
