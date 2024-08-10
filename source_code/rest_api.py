from fastapi import FastAPI
from sensors import Dht_22
from constants import DATABASE
from helpers import fetch_database
import sqlite3
import json


app = FastAPI()

# Get data from sqlite db
@app.get('/sensors/dht_22')
def get_dht22(from_date:str):
    """ 
    from_date: Get the data from a specific date untill nowi 
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
    
