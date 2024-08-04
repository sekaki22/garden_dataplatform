import time 
import adafruit_dht
import board
import os
import sqlite3
from datetime import datetime

# Configure board & dht device
dht_device = adafruit_dht.DHT22(board.D4, use_pulseio = False)
clear = lambda: os.system('clear')	
date_format = "%Y-%m-%d %H:%M:%S" 
clear = lambda: os.system('clear')

# Database insert statement
insert_string = """
INSERT INTO dht_22 (date_time, temp_c, humidity_perc)
VALUES (?, ?, ?)
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
        # Read dht values and store in tuple 
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        database_input = (datetime_now, temperature, humidity)
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
        print("Exception encountered")
        print(e)
