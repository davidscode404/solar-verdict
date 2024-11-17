import streamlit as st
import pandas as pd
import numpy as np
from get_info import get_info
from get_averages import calculate_weather_averages
from llama_prompt import llama_prompt

# Initialize session state for all variables
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'air_temp_avg' not in st.session_state:
    st.session_state.air_temp_avg = 0
if 'dni_avg' not in st.session_state:
    st.session_state.dni_avg = 0
if 'ghi_avg' not in st.session_state:
    st.session_state.ghi_avg = 0
if 'map_location' not in st.session_state:
    st.session_state.map_location = None

# Function to update averages and get AI response when button is clicked
def update_averages():
    data = pd.read_csv("weather_data.csv")
    air_temp = data.iloc[:, -3]
    dni = data.iloc[:, -2]
    ghi = data.iloc[:, -1]
    st.session_state.air_temp_avg = air_temp.mean()
    st.session_state.dni_avg = dni.mean()
    st.session_state.ghi_avg = ghi.mean()
    
    # Create the prompt with the current averages
    prompt = "Annual averages of 18.38 air temperature, 226.29 DNI and 196.39 GHI. In less than 50 words, Are solar panels worth it? How much money and energy could one save with solar panels?"
    #prompt = f"This location has an annual average of {st.session_state.air_temp_avg:.2f} air temperature, {st.session_state.dni_avg:.2f} DNI and {st.session_state.ghi_avg:.2f} GHI. How much money and energy could one save by installing solar panels?"

    try:
        # Get AI response using llama_prompt
        response = llama_prompt(prompt)  # Modified to accept prompt as parameter
        st.session_state.message = response
    except Exception as e:
        st.session_state.message = f"Error getting AI response: {str(e)}"
    
    st.session_state.map_location = pd.DataFrame({
        'lat': [-33.856784],
        'lon': [151.215297]
    })
    # Call calculate_weather_averages
    calculate_weather_averages('weather_data.csv')

# Function to reset everything
def reset_all():
    st.session_state.message = ""
    st.session_state.air_temp_avg = 0
    st.session_state.dni_avg = 0
    st.session_state.ghi_avg = 0
    st.session_state.map_location = None

st.set_page_config(
    page_title="SolarVerdict",
    layout="wide",
    page_icon="🌐")
#st.write("### SolarVerdict")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@300&display=swap');
        .custom-font {
            font-family: 'Roboto', sans-serif;
            font-size: 28px;
            font-weight: 300;
        }
    </style>
    <div class='custom-font'>SolarVerdict</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

with col1:
    # Create a container with relative positioning
    st.markdown("""
    <div style="position: relative;">
    <div style="position: absolute; top: 50px; left: 50px; z-index: 1;">
    """, unsafe_allow_html=True)
    
    # Close the positioning div
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add the image
    st.image("world.png", width=600)
    st.markdown("</div>", unsafe_allow_html=True)
    # Create a row for the buttons using columns
    button_col1, button_col2 = st.columns(2)
    
    # Add the buttons in separate columns
    with button_col1:
        st.button("▶️", on_click=update_averages)
    with button_col2:
        st.button("🔁", on_click=reset_all, type="secondary")

with col2:
    # Only show map if location is set
    if st.session_state.map_location is not None:
        #st.map(st.session_state.map_location, use_container_width=True)
        st.map(st.session_state.map_location, width=200, height=300)# use_container_width=True)
    else:
        # Create an empty container with the same height as the map
        st.markdown(
            """
            <div style="height: 300px; background-color: #f0f2f6; border-radius: 4px; display: flex; justify-content: center; align-items: center;">
                <p style="color: #666;">Select a location to begin.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Add the message box between maps and averages
st.text_area("AI Consultant 🤖", value=st.session_state.message, height=200, disabled=True, label_visibility="visible", help="With these annual average air temperature, DNI and GHI values, how much money and energy could one save by installing solar panels?")

st.write("### Averages:")
air_temp, dni, ghi = st.columns(3)
air_temp.metric(
    label="Air Temperature (°C)", 
    value=f"{st.session_state.air_temp_avg:,.2f}"
)
dni.metric(
    label=":information_source: DNI (Direct Normal Irradiance)", 
    value=f"{st.session_state.dni_avg:,.0f}",
    help="Direct Normal Irradiance (DNI) is the amount of solar radiation received per unit area by a surface that is always held perpendicular to the rays that come in a straight line from the direction of the sun."
)
ghi.metric(
    label=":information_source: GHI (Global Horizontal Irradiance)", 
    value=f"{st.session_state.ghi_avg:,.0f}",
    help="Global Horizontal Irradiance (GHI) is the total amount of shortwave radiation received from above by a surface horizontal to the ground, including both direct and diffuse solar radiation."
)
