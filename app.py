import streamlit as st
import json
import os
from weather_api import call_geo_code, call_weather 
weather_codes = {
	"0": "Clear sky",
	"1": "Mainly clear",
	"2": "Partly cloudy",
	"3": "Overcast",
    "48": "Depositing rime fog",
	"45": "Fog",
	"51": "Light drizzle",
	"53": "Moderate drizzle",
	"55": "Dense drizzle",
	"56": "Light freezing drizzle",
	"57": "Dense freezing drizzle",
	"61": "Slight rain",
	"63": "Moderate rain",
	"65": "Heavy rain",
	"66": "Light freezing rain",
	"67": "Heavy freezing rain",
	"71": "Slight snowfall",
	"73": "Moderate snowfall",
	"75": "Heavy snowfall",
	"77": "Snow grains",
	"80": "Slight rain showers",
	"81": "Moderate rain showers",
	"82": "Violent rain showers",
	"85": "Slight snow showers",
	"86": "Heavy snow showers",
	"95": "Thunderstorm",
	"96": "Thunderstorm with slight hail",
	"97": "Heavy thunderstorm",
	"99": "Thunderstorm with heavy hail"

}
st.set_page_config(
    page_title = "No Name Yet",
    page_icon= "🌤️",
    layout="wide"

)
if "cities" not in st.session_state:
    st.session_state.cities = []
if "search_status" not in st.session_state:
    st.session_state.search_status = False
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
st.markdown("""
<style>
.current-weather-card{
    width: 100%;
    background-color: #1F2937;
    padding: 20px;
    border-radius: 12px;
    color: #F9FAFB;
    border-left: 5px solid #38BDF8;
    margin-bottom: 20px;
    
}
.weather-data-card{
    background-color:#1F2937;
    padding: 20px;
    border-radius: 12px;
    color: #F9FAFB;
    border-left: 5px solid #38BDF8;
    margin-bottom: 20px;
}
.stApp{
    background-color: #0B1120;
}
h1, h2, h3, p {
     color: #F8FAFC !important;
}
[data-testid = "stSpinner"]{
    color: #F8FAFC;
}
[data-testid ="stSidebar"]{
    background-color:#111827;
    color:#F8FAFC;
    accent-color:#38BDF8;
    border-color:#263449;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color:#F8FAFC !important;
}
</style>
""", unsafe_allow_html = True)
st.sidebar.title("Explore")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard","No Name AI Assistant"],
    
)
if page == "Dashboard":
    st.title("DASHBOARD")

    if not st.session_state.search_status:

        with st.form("city_search"):
            city = st.text_input(
                "Search for a city",
                placeholder="e.g London"
            )

            submitted = st.form_submit_button("Search")

        if submitted:
            if not city.strip():
                st.warning("Please enter a city.")

            else:
                try:
                    with st.spinner("Searching for city..."):
                        coordinates = call_geo_code(city)

                        if coordinates is None:
                            st.error("City not found!")

                        else:
                            st.session_state.cities.append(city)
                            latitude = coordinates[0]
                            longitude = coordinates[1]
                            data = call_weather(latitude, longitude)

                            if data is None or "current" not in data:
                                st.error("Unable to retrieve weather!")

                            else:
                                st.session_state.search_query = city
                                st.session_state.search_status = True
                                

                                st.rerun()

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    else:
        
        city = st.session_state.search_query
        with st.spinner("Loading..."):
            coordinates = call_geo_code(city)

            if coordinates is not None:
                latitude = coordinates[0]
                longitude = coordinates[1]
                data = call_weather(latitude, longitude)

                if data is not None and "current" in data:

                    temperature = data["current"]["temperature_2m"]
                    humidity = data["current"]["relative_humidity_2m"]
                    feel_like_temp = data["current"]["apparent_temperature"]
                    wind_speed = data["current"]["wind_speed_10m"]
                    uv_index = data["current"]["uv_index"]
                    weather_code_num = data["current"]["weather_code"]

                    condition = weather_codes.get(
                        str(weather_code_num),
                        "Unknown Weather Code"
                    )
                    
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 12px; color: gray;">
                            Weather data by
                            <a href="https://open-meteo.com/"
                                target="_blank"
                                style="color: gray;">
                                Open-Meteo.com
                            </a>
                            |
                             <a href="https://creativecommons.org/licenses/by/4.0/"
                                target="_blank"
                                style="color: gray;">
                                CC BY 4.0
                            </a>
                        </div>
                        """,
                    unsafe_allow_html=True
                )


                    st.markdown(f"""
                    <div class="current-weather-card">
                        <h2>{temperature}F</h2>
                        <p>{condition}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class="weather-data-card">
                            <h2>{humidity} %</h2>
                            <p>Humidity</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="weather-data-card">
                            <h2>{feel_like_temp} °F</h2>
                            <p>Feels Like</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Unable to retrieve weather!")
            else:
                st.error("City not found!")
        options = ["Choose another city"] + st.session_state.cities
        choice = st.selectbox(
            "History",
            options,
            index = None,
            placeholder = "Choose a city"
        )
        if choice == "Choose another city":
            st.session_state.search_status = False
            st.session_state.search_query = ""

            

            st.rerun()
        elif choice is not None and choice != st.session_state.search_query:
            st.session_state.search_query = choice
            st.session_state.search_status = True
            st.rerun()

else:
    st.title("Meet AI Assistant")

