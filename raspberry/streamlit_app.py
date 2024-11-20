import streamlit as st
import streamlit_shadcn_ui as ui
from constants import DATABASE, time_options
from helpers import plot_timeseries, get_last_value, get_time_range, plot_lux_timeseries, plot_soil_moisture_timeseries
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Home", page_icon=":house:")

st.title("Kelly's garden dashboard")

st.write("""
         This dashboard will display the values of different metrics measures
         in Kellys' vegetable garden :tomato: :eggplant: :hot_pepper: :pear:
        """)

col1, col2 = st.columns(2)

# For this page I just want to get the latest values for some sensors
temp_now, temp_timestamp = get_last_value("dht_22", "temp_c")
humidity_now, humidity_timestamp = get_last_value("dht_22", " humidity_perc")
lux_now, lux_timestamp = get_last_value("tsl_2591", " lux")
soil_now, soil_timestamp = get_last_value("soil_moisture_sens", " raw_value")


# Place the widgets above the plot to avoid reloading the plot when the slider is moved     
with col1:

    # Card for temperature
    temperature_card = \
    ui.metric_card(title="Temperature", 
                    content=f"{temp_now} degrees Celsius", 
                    description=f"Last measurement: {temp_timestamp}",
                    key="current_temp")

    # Card for lux
    ui.metric_card(title="Light intensity", 
                    content=f"{lux_now} lux units", 
                    description=f"Last measurement: {lux_timestamp}",
                    key="current_lux")    


with col2:

    # Card for humidity
    humidity_card = \
    ui.metric_card(title="Humidity",
                    content=f"{humidity_now} %",
                    description=f"Last measurement: {humidity_timestamp}",
                    key="current_hum")


    # Card for soil moisture
    ui.metric_card(title="Soil moisture",
                    content=f"{soil_now} Millivolts",
                    description=f"Last measurement: {soil_timestamp}",
                    key="current_soil")
    
st.image("static/images/garden_yield.jpeg")
    

