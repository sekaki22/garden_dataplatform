import streamlit as st
from constants import DATABASE,time_options
from helpers import plot_lux_timeseries, get_time_range, get_last_value
import plotly.express as px
import streamlit_shadcn_ui as ui
from datetime import datetime, timedelta

st.set_page_config(page_title="TSL2591", page_icon=":sunny:")

st.title("TSL2591")

st.write("""
         Sensor that measures light intensity in lux values. A higher value means
         more intense sunshine
        """)

   # Radio button for lux
lux_range = st.radio(
        "Select time range for Lux",
        options=list(time_options.keys()),
        key="lux_time_range"
    )
since_lux, until_lux = get_time_range(lux_range, time_options)
fig_lux = plot_lux_timeseries("tsl_2591", DATABASE, "lux", since_lux, until_lux, "Brightness", (0, 50000))
st.plotly_chart(fig_lux)

