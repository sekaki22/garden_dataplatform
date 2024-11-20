import streamlit as st
from constants import DATABASE,time_options
from helpers import plot_soil_moisture_timeseries, get_time_range, get_last_value
import plotly.express as px
import streamlit_shadcn_ui as ui
from datetime import datetime, timedelta

st.set_page_config(page_title="soil moisture", page_icon=":potted_plant:")

st.title("Soil moisture sensor")

st.write("""
         Sensor that measures the moisture in the ground. Measurement are in
         millivolts. The higher the value, the dryer the environment (which seems
         contra-intuitive)
        """)

# Radio button for soil moisture
soil_range = st.radio(
    "Select time range for Soil Moisture",
    options=list(time_options.keys()),
    key="soil_time_range"
)
since_soil, until_soil = get_time_range(soil_range, time_options)
fig_soil = plot_soil_moisture_timeseries("soil_moisture_sens", DATABASE, "raw_value", since_soil, until_soil, "Soil Moisture in milli volts")
st.plotly_chart(fig_soil)

