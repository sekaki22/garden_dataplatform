import sqlite3

DATABASE = "../raspberry_sensors.db" 

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

create_table_statement = """
CREATE TABLE IF NOT EXISTS dht_22
(id INTEGER PRIMARY KEY AUTOINCREMENT,
date_time DATETIME,
temp_c REAL,
humidity_perc REAL)
"""


cursor.execute(create_table_statement)

conn.commit()
conn.close()


