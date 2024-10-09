import sqlite3
import pandas as pd
import plotly.express as px

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


def plot_timeseries(tablename: str, database_file: str, column_name: str,
                    top_n_records: int):
    """
    args:
    tablename: Sqlite3 table name of specific sensor
    """

    # Connect to SQLite db
    conn = sqlite3.connect(database_file)
    
    #Query data with pandas method
    query = f"SELECT * FROM {tablename} ORDER BY date_time DESC LIMIT {top_n_records}"
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    fig = px.line(df, x='date_time', y=column_name, title = f"{column_name} over time")
    fig.update_layout(xaxis_title="Date and time", yaxis_title= column_name)
    
    return fig
