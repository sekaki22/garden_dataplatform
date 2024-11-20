from datetime import datetime, timedelta
# Constants

#sqlite database location
DATABASE = "/home/selim/raspberry_sensors.db" 

# Define time range options
time_options = {
    "Last Hour": timedelta(hours=1),
    "Last Day": timedelta(days=1),
    "Last Week": timedelta(weeks=1),
    "Last Month": timedelta(days=30)
}


