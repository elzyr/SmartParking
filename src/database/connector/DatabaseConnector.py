import configparser
import mysql.connector
import logging

class DatabaseConnector:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.host = config['mysql']['host']
        self.user = config['mysql']['user']
        self.password = config['mysql']['password']
        self.database = config['mysql']['database']
        self.port = config['mysql'].getint('port', 3306)
        self.connection = None
        logging.info('DatabaseConnector object created')
        logging.info(f'Host: {self.host}')
        logging.info(f'User: {self.user}')
        logging.info(f'Database: {self.database}')
        logging.info(f'Port: {self.port}')
        logging.info(f'Password: {self.password}')

    def connect(self):
        try:
            logging.info('Attempting to connect to the database...')
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                logging.info('Connected to MySQL database')
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            self.connection = None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def get_data(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert_data(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def update_data(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def delete_data(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
