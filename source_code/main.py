import constants
import sensors
import sqlite3
import board
import time
import os

clear = lambda: os.system('clear')	
date_format = "%Y-%m-%d %H:%M:%S" 


# Connect to database
conn = sqlite3.connect(constants.DATABASE)
cursor = conn.cursor()

# Initialize sensors
dht = sensors.Dht_22(pinout = board.D4, db_path = constants.DATABASE) 
tsl = sensors.Tsl_2591(db_path = constants.DATABASE)

# Run while loop

while(True):
    try:
        # Read, print and write dht values
        dht.read_data()
        dht.print_values()
        dht.write_to_db(cursor)        
        # Read, print and write tsl values
        tsl.read_data()
        tsl.print_values()
        tsl.write_to_db(cursor)
        time.sleep(5)
        conn.commit()
        clear()
    except Exception as e:
        print(f"Following exception encountered: \n {e}")
    

