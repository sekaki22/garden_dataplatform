import streamlit as st
from constants import DATABASE,time_options
from helpers import plot_timeseries, get_time_range, get_last_value
import plotly.express as px
import streamlit_shadcn_ui as ui
from datetime import datetime, timedelta

st.set_page_config(page_title="DHT22", page_icon=":partly_sunny:")

st.title("DHT 22")

st.write("""
         Sensor that measures temperature and humidity
        """)

col1, col2 = st.columns(2)



temp_now, temp_timestamp = get_last_value("dht_22", "temp_c")
humidity_now, humidity_timestamp = get_last_value("dht_22", " humidity_perc")

with col1:
# Radio button for temperature
    temp_range = st.radio(
        "Select time range for Temperature",
        options=list(time_options.keys()),
        key="temp_time_range"
    )
    since_temp, until_temp = get_time_range(temp_range, time_options)
    fig_temp = plot_timeseries("dht_22", DATABASE, "temp_c", since_temp, until_temp, "Temperature in Celsius")
    st.plotly_chart(fig_temp)


with col2:

    # Radio button for humidity
    hum_range = st.radio(
        "Select time range for Humidity",
        options=list(time_options.keys()),
        key="hum_time_range"
    )
    since_hum, until_hum = get_time_range(hum_range, time_options)
    fig_hum = plot_timeseries("dht_22", DATABASE, "humidity_perc", since_hum, until_hum, "Humidity Percentage", (40, 100))
    st.plotly_chart(fig_hum)