import sqlite3
from constants import DATABASE

# Connect to local db
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create table statement dht22
create_table_statement_dht = """
CREATE TABLE IF NOT EXISTS dht_22
(id INTEGER PRIMARY KEY AUTOINCREMENT,
date_time DATETIME,
temp_c REAL,
humidity_perc REAL);
"""

# Create table statement tsl_2591
create_table_statement_tsl = """
CREATE TABLE IF NOT EXISTS tsl_2591
(id INTEGER PRIMARY KEY AUTOINCREMENT,
date_time DATETIME,
lux REAL,
visibility INTEGER,
infrared INTEGER);
"""

# Create table statement RAINDROP_SENS
create_table_statement_rs = """
CREATE TABLE IF NOT EXISTS raindrop_sens
(id INTEGER PRIMARY KEY AUTOINCREMENT,
date_time DATETIME,
raw_value REAL);
"""

# Create table statement Soil Moisture 
create_table_statement_sm = """
CREATE TABLE IF NOT EXISTS soil_moisture_sens
(id INTEGER PRIMARY KEY AUTOINCREMENT,
date_time DATETIME,
raw_value REAL);
"""

# Execute statements on database file
sql_statements = [create_table_statement_dht, create_table_statement_tsl, 
                  create_table_statement_rs, create_table_statement_sm]

for sql_statement in sql_statements:
    cursor.execute(sql_statement)

conn.commit()
conn.close()


