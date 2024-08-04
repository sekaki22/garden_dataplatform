import time 
import adafruit_dht
import adafruit_tsl2591
import board
import sqlite3
from datetime import datetime
from constants import DATABASE


class Dht_22:
    def __init__(self, pinout = board.D4, db_path = DATABASE):
        self.config = adafruit_dht.DHT22(pinout, use_pulseio = False)
        self.db_path = db_path
        self.temperature = None
        self.humidity = None

    def read_data(self):
        self.temperature = self.config.temperature
        self.humidity = self.config.humidity

    def write_to_db(self, cursor):
        # Database insert statement
        insert_string = """
        INSERT INTO dht_22 (date_time, temp_c, humidity_perc)
        VALUES (?, ?, ?)
        """ 
        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        database_input = (datetime_now, self.temperature, 
                            self.humidity)
        cursor.execute(insert_string, database_input)

    def print_values(self):
        print(f"Temperature: {self.temperature} Celsius")
        print(f"Humidity: {self.humidity}")

 
class Tsl_2591:
    def __init__(self, db_path = DATABASE):
        self.config = adafruit_tsl2591.TSL2591(board.I2C())        
        self.db_path = db_path
        self.lux = None
        self.visibility = None
        self.infrared = None

    def read_data(self):
        self.lux = self.config.lux
        self.visibility = self.config.visible
        self.infrared = self.config.infrared

    def write_to_db(self, cursor):
        # Database insert statement
        insert_string = """
        INSERT INTO tsl_2591 (date_time, lux, visibility, infrared)
        VALUES (?, ?, ?, ?)
         """ 

        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        database_input = (datetime_now, self.lux, self.visibility, self.infrared)
        cursor.execute(insert_string, database_input)

    def print_values(self):
        print(f"Lux: {self.lux}")
        print(f"Visibility: {self.visibility}")
        print(f"Infrared: {self.infrared}\n")

 
