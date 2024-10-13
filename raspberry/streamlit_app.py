import streamlit as st
from constants import DATABASE
from helpers import plot_timeseries 
import plotly.express as px
from datetime import datetime, timedelta

st.title("Kelly's garden dashboard")

st.write("""
         This dashboard will display the values of different metrics measures
         in Kellys' vegetable garden :tomato: :eggplant: :hot_pepper: :pear:
        """)

col1, col2 = st.columns(2)

# Place the widgets above the plot to avoid reloading the plot when the slider is moved     
with col1:
    # Datetime range slider for temperature
    since_temp, until_temp = st.slider(
        "Select datetime range for Temperature",
        value=(datetime.now() - timedelta(hours=1), datetime.now()),
        format="MM/DD/YY - HH:mm",
        key="temp_datetime_range"
    )
    fig_temp = plot_timeseries("dht_22", DATABASE, "temperature in Celsius", since_temp, until_temp)
    st.plotly_chart(fig_temp)

    since_hum, until_hum = st.slider(
    "Select datetime range for Humidity",
    value=(datetime.now() - timedelta(hours=1), datetime.now()),
    format="MM/DD/YY - HH:mm",
    key="hum_datetime_range"
    )
    
    # Datetime range slider for humidit
    fig_hum = plot_timeseries("dht_22", DATABASE, "humidity %", since_hum, until_hum)
    st.plotly_chart(fig_hum)



with col2:
    # Datetime range slider for lux
    since_lux, until_lux = st.slider(
    "Select datetime range for Lux",
    value=(datetime.now() - timedelta(hours=1), datetime.now()),
    format="MM/DD/YY - HH:mm",
    key="lux_datetime_range"
)

    fig_lux = plot_timeseries("tsl_2591", DATABASE, "lux", since_lux, until_lux)
    st.plotly_chart(fig_lux)

    since_soil, until_soil = st.slider(
    "Select datetime range for Soil Moisture",
    value=(datetime.now() - timedelta(hours=1), datetime.now()),
    format="MM/DD/YY - HH:mm",
    key="soil_datetime_range"
)
    # Datetime range slider for soil moistur
    fig_soil = plot_timeseries("soil_moisture_sens", DATABASE, "milli voltage", since_soil, until_soil)
    st.plotly_chart(fig_soil)


