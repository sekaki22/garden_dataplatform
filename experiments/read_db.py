import sqlite3
import json

DATABASE = "/home/selimberntsen/raspberry_sensors.db" 

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()







def fetch_database(cursor, query):
    
    # Execute query to database and use fetchall
    cursor.execute(query)
    rows = cursor.fetchall()

    # List column names
    columns = [column[0] for column in cursor.description]
    
    
    results = []

    for row in rows:
        results.append(dict(zip(columns, row)))
    
    return results

results = fetch_database(cursor, select_string)

print(results)



