from src.database.connector.DatabaseConnector import DatabaseConnector
import logging

from src.database.repository.CarRepository import CarRepository
from src.database.model.Car import Car

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

