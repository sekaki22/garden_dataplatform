import sqlite3

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


