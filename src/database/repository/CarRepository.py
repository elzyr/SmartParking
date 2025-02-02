import logging
import mysql.connector
from src.database.model.Car import Car

class CarRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def insert_car(self, car):
        try:
            cursor = self.db_connector.connection.cursor()
            query = "INSERT INTO cars (registration, color) VALUES (%s, %s)"
            cursor.execute(query, (car.registration, car.color))
            self.db_connector.connection.commit()
            cursor.close()
            logging.info('Car inserted into the database')
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def get_cars(self):
        try:
            cursor = self.db_connector.connection.cursor()
            query = "SELECT registration, color FROM cars"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            cars = [Car(registration=row[0], color=row[1]) for row in result]
            logging.info('Cars retrieved from the database')
            return cars
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return []

    def delete_car(self, registration):
        try:
            cursor = self.db_connector.connection.cursor()
            query = "DELETE FROM cars WHERE registration = %s"
            cursor.execute(query, (registration,))
            self.db_connector.connection.commit()
            cursor.close()
            logging.info(f'Car with registration {registration} deleted from the database')
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def delete_all_cars(self):
        try:
            cursor = self.db_connector.connection.cursor()
            query = "DELETE FROM cars"
            cursor.execute(query)
            self.db_connector.connection.commit()
            cursor.close()
            logging.info('All cars deleted from the database')
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def check_plate_in_database(self, plate_number):
        print('Checking if plate is in database')
        try:
            cursor = self.db_connector.connection.cursor()
            query = f"SELECT * FROM CARS WHERE registration = '{plate_number}'"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            logging.error(f"Błąd bazy danych: {err}")
            return False

    def car_incidents(self,color1, color2, description):
        try:
            cursor = self.db_connector.connection.cursor()
            query = "INSERT INTO car_logs (color_car1, color_car2,description) VALUES (%s, %s, %s)"
            cursor.execute(query, (color1, color2, description))
            self.db_connector.connection.commit()
            cursor.close()
            logging.info('Added incident to the database')

        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")

