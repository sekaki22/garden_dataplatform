import streamlit as st
from constants import DATABASE
from helpers import plot_timeseries
import plotly.express as px 
from datetime import datetime, timedelta

# Add streamlit date picker for since and untill date
since_date = st.date_input("Since date", value=datetime.now())
untill_date = st.date_input("Until date", value=datetime.now())

st.title("Kelly's garden dashboard")

st.write("""
         This dashboard will display the values of different metrics measures
         in Kellys' vegetable garden :tomato: :eggplant: :hot_pepper: :pear:
        """)

col1, col2 = st.columns(2)

with col1:
    since_temp = st.date_input(
        "Since date for Temperature",
        value=datetime.now() - timedelta(hours=1),
        key="since_temp"
    )
    until_temp = st.date_input(
        "Until date for Temperature",
        value=datetime.now(),
        key="until_temp"
    )
    fig_temp = plot_timeseries("dht_22", DATABASE, "temp_c", since_temp, until_temp)
    st.plotly_chart(fig_temp)

    # Date range selector for humidity
    since_hum = st.date_input(
        "Since date for Humidity",
        value=datetime.now() - timedelta(hours=1),
        key="since_hum"
    )
    until_hum = st.date_input(
        "Until date for Humidity",
        value=datetime.now(),
        key="until_hum"
    )
    # Fill in proper since and untill parameters
    fig_hum = plot_timeseries("dht_22", DATABASE, "humidity_perc", since_hum, until_hum)
    st.plotly_chart(fig_hum)

with col2:
    # Date range selector for lux
    since_lux = st.date_input(
        "Since date for Lux",
        value=datetime.now() - timedelta(hours=1),
        key="since_lux"
    )
    until_lux = st.date_input(
        "Until date for Lux",
        value=datetime.now(),
        key="until_lux"
    )
    fig_lux = plot_timeseries("tsl_2591", DATABASE, "lux", since_lux, until_lux)
    st.plotly_chart(fig_lux)
    
    # Date range selector for soil moisture
    since_soil = st.date_input(
        "Since date for Soil Moisture",
        value=datetime.now() - timedelta(hours=1),
        key="since_soil"
    )
    until_soil = st.date_input(
        "Until date for Soil Moisture",
        value=datetime.now(),
        key="until_soil"
    )
    fig_soil = plot_timeseries("soil_moisture_sens", DATABASE, "raw_value", since_soil, until_soil)
    st.plotly_chart(fig_soil)


