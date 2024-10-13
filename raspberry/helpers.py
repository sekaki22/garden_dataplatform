import sqlite3
import pandas as pd
import plotly.express as px

# Add docstring to the function with description, args, returns, raises, etc.           
#          
def fetch_database(cursor, query):
    """
    Fetch data from SQLite database and return data for fastapi response

    args:
    cursor: sqlite3 cursor object
    query: sql query
    
    returns:
    results: list of dictionaries with column names as keys and row values as values
    """
    
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
                    since_date: str, untill_date: str):
    """
    Plot timeseries data from SQLite database sensor data

    args:
    tablename: Sqlite3 table name of specific sensor
    database_file: path to SQLite database file
    column_name: name of the column to plot
    since_date: start date for the plot
    untill_date: end date for the plot
    
    returns:
    fig: plotly figure object
    """

    # Connect to SQLite db
    conn = sqlite3.connect(database_file)
    
    #Query data with pandas method
    query = f"SELECT * FROM {tablename} WHERE date_time > datetime('{since_date}') AND date_time < datetime('{untill_date}')"
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    fig = px.line(df, x='date_time', y=column_name, title = f"{column_name} over time")
    fig.update_layout(xaxis_title="Date and time", yaxis_title= column_name)
    
    return fig

