from fastapi import FastAPI, Query
from constants import DATABASE
from helpers import fetch_database
import sqlite3
import json
from sensor_models import DHT22, TSL2591, BasicAnalogSensor
from datetime import datetime

app = FastAPI()


@app.get("/")
def root_test():
    return {"response": "server is online"}


# Get data from sqlite db
@app.get('/sensors/dht22')
def get_dht22(from_date:str):
    """ 
    from_date: Get the data from a specific date untill now
    
    returns: json data dump 
    """
    # Create a cursor
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = f"""
    SELECT id, date_time, temp_c, humidity_perc
    FROM dht_22
    WHERE date_time > '{from_date}'
    """
    results = fetch_database(cursor, query)

    return json.dumps(results, indent=4)

# Post data to sqlite db
@app.post('/sensors/dht22')
def post_dht22(instance: DHT22):
    """
    Process post requests by ingesting payload into database
    """    
    
    # Create a cursor
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = f"""
            INSERT INTO dht_22 (date_time, temp_c, humidity_perc)
            VALUES (?, ?, ?)
            """ 
   
    # Create database input
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database_input = (datetime_now, instance.temperature, 
                            instance.humidity)
    # Execute and commit :)
    cursor.execute(query, database_input)
    conn.commit() 
    
    return "200: Data was ingested into database"


@app.post('/sensors/tsl2591')
def post_tsl2591(instance: TSL2591):
    """
    Process post requests by ingesting payload into database
    """    
    
    # Create a cursor
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = f"""
            INSERT INTO tsl_2591 (date_time, lux, visibility,
                                infrared)
            VALUES (?, ?, ?, ?)
            """ 
   
    # Create database input
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database_input = (datetime_now, instance.lux, 
                      instance.visibility, instance.infrared)
    # Execute and commit :)
    cursor.execute(query, database_input)
    conn.commit() 
    
    return "200: Data was ingested into database"

@app.post('/sensors/analog_inputs')
def post_analog(instance: BasicAnalogSensor, table_name: str):
    """
    Process post requests by ingesting payload into database
    """    
    
    # Create a cursor
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = f"""
            INSERT INTO {table_name} (date_time, raw_value)
            VALUES (?, ?)
            """ 
   
    # Create database input
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database_input = (datetime_now, instance.analog_value)
    # Execute and commit :)
    cursor.execute(query, database_input)
    conn.commit() 
    
    return "200: Data was ingested into database"


# Return the last record og any given sensor
@app.get('/sensors/{sensor_name}/last_value')
async def return_last_value(sensor_name:str):
    """ 
    sensor_name: The name of the sensor you want the latest file from
    
    returns: most recent record in json form 
    """
    # Create a cursor
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = f"""
    SELECT *
    FROM {sensor_name}
    ORDER BY id DESC LIMIT 1
    """
    results = fetch_database(cursor, query)
    
    return json.dumps(results, indent=4)

