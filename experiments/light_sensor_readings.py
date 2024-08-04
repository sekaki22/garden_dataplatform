import board
import time
import os
import sqlite3
import adafruit_tsl2591
from datetime import datetime

# Configure board & I2C bus (gpio inputs)
i2c = board.I2C()
sensor = adafruit_tsl2591.TSL2591(i2c)
date_format = "%Y-%m-%d %H:%M:%S" 
clear = lambda: os.system('clear')

# Database insert statement
insert_string = """
INSERT INTO tsl_2591 (date_time, lux, visibility, infrared)
VALUES (?, ?, ?, ?)
""" 

# Open connection to local db
conn = sqlite3.connect('../../raspberry_sensors.db')
cursor = conn.cursor()

i = 0

# Loops infinitely
while(True):
    try:
         #Set datetime
         datetime_now = datetime.now().strftime(date_format) 
         # Read tsl values and store in tuple 
         database_input = (datetime_now, sensor.lux, sensor.visible, sensor.infrared)
         print(database_input)

         # Execute Insert statement in db
         cursor.execute(insert_string, database_input)
         conn.commit()

         # Sleep & Repeat
         time.sleep(10)
         i+=1
         if i % 10 == 0:
             conn.close()
             conn = sqlite3.connect('../../raspberry_sensors.db')
             cursor = conn.cursor()
    except Exception as e:
        print(f"The following error occured:\n (e)")
