import streamlit as st
from constants import DATABASE
from helpers import plot_timeseries, get_time_range, plot_lux_timeseries, plot_soil_moisture_timeseries
import plotly.express as px
from datetime import datetime, timedelta

st.title("Kelly's garden dashboard")

st.write("""
         This dashboard will display the values of different metrics measures
         in Kellys' vegetable garden :tomato: :eggplant: :hot_pepper: :pear:
        """)

col1, col2 = st.columns(2)

# Define time range options
time_options = {
    "Last Hour": timedelta(hours=1),
    "Last Day": timedelta(days=1),
    "Last Week": timedelta(weeks=1),
    "Last Month": timedelta(days=30)
}

# Place the widgets above the plot to avoid reloading the plot when the slider is moved     
with col1:

    # Add voltage sensor timeseries
    voltage_range = st.radio(
        "Select time range for Voltage",
        options=list(time_options.keys()),
        key="voltage_time_range"
    )
    since_voltage, until_voltage = get_time_range(voltage_range, time_options)
    fig_voltage = plot_timeseries("voltage_sens", DATABASE, "converted_voltage", since_voltage, until_voltage, "Battery Voltage", (0, 7))
    st.plotly_chart(fig_voltage)

    # Radio button for temperature
    temp_range = st.radio(
        "Select time range for Temperature",
        options=list(time_options.keys()),
        key="temp_time_range"
    )
    since_temp, until_temp = get_time_range(temp_range, time_options)
    fig_temp = plot_timeseries("dht_22", DATABASE, "temp_c", since_temp, until_temp, "Temperature in Celsius")
    st.plotly_chart(fig_temp)

     # Radio button for lux
    lux_range = st.radio(
        "Select time range for Lux",
        options=list(time_options.keys()),
        key="lux_time_range"
    )
    since_lux, until_lux = get_time_range(lux_range, time_options)
    fig_lux = plot_lux_timeseries("tsl_2591", DATABASE, "lux", since_lux, until_lux, "Brightness", (0, 50000))
    st.plotly_chart(fig_lux)

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


    # Radio button for soil moisture
    soil_range = st.radio(
        "Select time range for Soil Moisture",
        options=list(time_options.keys()),
        key="soil_time_range"
    )
    since_soil, until_soil = get_time_range(soil_range, time_options)
    fig_soil = plot_soil_moisture_timeseries("soil_moisture_sens", DATABASE, "raw_value", since_soil, until_soil, "Soil Moisture in milli volts")
    st.plotly_chart(fig_soil)


