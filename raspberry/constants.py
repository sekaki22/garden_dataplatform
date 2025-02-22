from datetime import datetime, timedelta
# Constants

#sqlite database location
DATABASE = "/home/selim/databases/esp32_sensors.db" 

#BLE Server UUID
BLE_SERVER_UUID = "8aff4410-808a-4ce2-af5c-4122e0e05860"

# Define time range options
time_options = {
    "Last Hour": timedelta(hours=1),
    "Last Day": timedelta(days=1),
    "Last Week": timedelta(weeks=1),
    "Last Month": timedelta(days=30)
}


