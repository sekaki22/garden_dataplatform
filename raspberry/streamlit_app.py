import streamlit as st
from constants import DATABASE
from helpers import plot_timeseries
import plotly.express as px

st.title("Kelly's garden dashboard")

st.write("""
         This dashboard will display the values of different metrics measures
         in Kellys' vegetable garden :tomato: :eggplant: :hot_pepper: :pear:
        """)

col1, col2 = st.columns(2)

with col1:
    fig_temp = plot_timeseries("dht_22", DATABASE, "temp_c", 100)
    st.plotly_chart(fig_temp)
    fig_hum = plot_timeseries("dht_22", DATABASE, "humidity_perc", 100)
    st.plotly_chart(fig_hum)

with col2:
    fig_lux = plot_timeseries("tsl_2591", DATABASE, "lux", 60)
    st.plotly_chart(fig_lux)
    fig_soil = plot_timeseries("soil_moisture_sens", DATABASE, "raw_value", 50)
    st.plotly_chart(fig_soil)


