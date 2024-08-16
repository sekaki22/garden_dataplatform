from fastapi import FastAPI
from sensors import Dht_22
from constants import DATABASE
from helpers import fetch_database
import sqlite3
import json
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class DHT22_Model(BaseModel):
    temperature: float
    humidity: float


# Get data from sqlite db
@app.get('/sensors/dht_22')
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
@app.post('/sensors/dht_22')
def post_dht22(instance: DHT22_Model):
    """
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

     
