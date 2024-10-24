import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

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

    # Function to get the time range based on selection
def get_time_range(selection, time_options):
    return datetime.now() - time_options[selection], datetime.now()


def plot_timeseries(sensor_type, database, metric, since, until, title, y_range=None):
    """
    Plot timeseries data from SQLite database sensor data

    args:
    sensor_type: Sqlite3 table name of specific sensor
    database: path to SQLite database file
    metric: name of the column to plot
    since: start date for the plot
    until: end date for the plot
    title: title of the plot
    y_range: tuple specifying the y-axis range (min, max)
    
    returns:
    fig: plotly figure object
    """

    # Connect to SQLite db
    conn = sqlite3.connect(database)
    
    # Query data with pandas method
    query = f"SELECT * FROM {sensor_type} WHERE date_time > datetime('{since}') AND date_time < datetime('{until}')"
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    fig = px.line(df, x='date_time', y=metric, title=title)
    fig.update_layout(xaxis_title="Date and time", yaxis_title=metric)
    
    if y_range:
        fig.update_yaxes(range=y_range)
    
    return fig


def plot_lux_timeseries(sensor_type, database, metric, since, until, title, y_range=None):
    """
    Plot timeseries data for lux with custom y-ticks

    args:
    sensor_type: Sqlite3 table name of specific sensor
    database: path to SQLite database file
    metric: name of the column to plot
    since: start date for the plot
    until: end date for the plot
    title: title of the plot
    y_range: tuple specifying the y-axis range (min, max)
    
    returns:
    fig: plotly figure object
    """

    # Connect to SQLite db
    conn = sqlite3.connect(database)
    
    # Query data with pandas method
    query = f"SELECT * FROM {sensor_type} WHERE date_time > datetime('{since}') AND date_time < datetime('{until}')"
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    fig = px.line(df, x='date_time', y=metric, title=title)
    fig.update_traces(line=dict(color='yellow'), fill='tozeroy', fillcolor='rgba(255, 255, 0, 0.3)')
    fig.update_layout(
        xaxis_title="Date and time", 
        yaxis_title=metric,
        yaxis=dict(
            tickvals=[1000, 5000, 10000, 30000],
            ticktext=["Shadow", "Indirect Light", "Bright Indirect Light", "Bright Direct Light"]
        )
    )
    
    if y_range:
        fig.update_yaxes(range=y_range)
    
    return fig

def plot_soil_moisture_timeseries(sensor_type, database, metric, since, until, title, y_range=None):
    """
    Plot timeseries data for soil moisture with custom y-ticks

    args:
    sensor_type: Sqlite3 table name of specific sensor
    database: path to SQLite database file
    metric: name of the column to plot
    since: start date for the plot
    until: end date for the plot
    title: title of the plot
    y_range: tuple specifying the y-axis range (min, max)
    
    returns:
    fig: plotly figure object
    """

    # Connect to SQLite db
    conn = sqlite3.connect(database)
    
    # Query data with pandas method
    query = f"SELECT * FROM {sensor_type} WHERE date_time > datetime('{since}') AND date_time < datetime('{until}')"
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    fig = px.line(df, x='date_time', y=metric, title=title)
    fig.update_traces(line=dict(color='blue'), fill='tonexty', fillcolor='rgba(0, 0, 255, 0.3)')
    fig.update_layout(
        xaxis_title="Date and time", 
        yaxis_title=metric,
        yaxis=dict(
            tickvals=[1000, 1200, 1800],
            ticktext=["Sufficiently Wet", "Water the Plants", "Water as Soon as Possible!"]
        ),
        plot_bgcolor='white'
    )
    
    if y_range:
        fig.update_yaxes(range=y_range)
    
    return fig
