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

# Execute statements on database file
table_statements = [create_table_statement_dht, create_table_statement_tsl]

for sql_statement in table_statements:
    cursor.execute(table_statement)

conn.commit()
conn.close()


