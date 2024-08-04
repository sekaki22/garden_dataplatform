import sqlite3

DATABASE = "../raspberry_sensors.db" 

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

create_table_statement = """
CREATE TABLE IF NOT EXISTS tsl_2591
(id INTEGER PRIMARY KEY AUTOINCREMENT,
date_time DATETIME,
lux REAL,
visibility INTEGER,
infrared INTEGER)
"""

test_tuple = ('2024-01-01 10:30:00', 0.0, 0, 0)

test_insert_statement = """
INSERT INTO tsl_2591 (date_time, lux, visibility, infrared)
VALUES (?, ?, ?, ?)
"""

cursor.execute(create_table_statement)
cursor.execute(test_insert_statement, test_tuple)

conn.commit()

conn.close()


