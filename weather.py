import streamlit as st
import requests


def get_weather(api_key, city, units):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        icon = data['weather'][0]['icon']
        return {
            'weather': weather,
            'temperature': temp,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'icon': icon
        }
    else:
        return None

def display_weather_info(weather_info, city, units):
    unit_symbol = "°C" if units == "metric" else "°F"
    st.write(f"## Weather in {city}")
    st.image(f"http://openweathermap.org/img/wn/{weather_info['icon']}@2x.png")
    st.write(f"**Description:** {weather_info['weather']}")
    st.write(f"**Temperature:** {weather_info['temperature']}{unit_symbol}")
    st.write(f"**Humidity:** {weather_info['humidity']}%")
    st.write(f"**Wind Speed:** {weather_info['wind_speed']} m/s")

    # Example of an alert based on weather conditions
    if weather_info['temperature'] > 35 and units == "metric":
        st.warning("🌞 It's very hot! Stay hydrated and avoid prolonged exposure to the sun.")
    elif weather_info['temperature'] < 0 and units == "metric":
        st.warning("❄️ It's freezing! Make sure to dress warmly.")
    if 'rain' in weather_info['weather'].lower():
        st.info("☔ It's raining. Don't forget to take an umbrella!")
    if 'snow' in weather_info['weather'].lower():
        st.info("❄️ Snowfall expected. Drive safely!")

def main():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    st.title("🌤️ Real-Time Weather Info App 🌤️")
    st.image("https://media.licdn.com/dms/image/D4E12AQGHerfLgiHI9Q/article-cover_image-shrink_720_1280/0/1700618292025?e=2147483647&v=beta&t=SNjgyf2IVFINmh9_5PJfF9Pbgwig5y5ytrtbw3uqD-c")
    st.write("Enter the name of any city to get the current weather information and alerts.")

    api_key = "7c8e37d0082cf3035641624f0d67c783"
    
    with st.form("weather_form"):
        user_input = st.text_input("Enter city name or ask about weather:", help="Enter the city name you want to check the weather for or ask a weather-related question.")
        units = st.radio("Units:", ('metric', 'imperial'), help="Select the units for temperature: Celsius (metric) or Fahrenheit (imperial).")
        submitted = st.form_submit_button("Get Weather")

    if submitted:
        city = get_city_from_text(user_input)
        if not city:
            city = user_input.strip()
        
        if city:
            weather_info = get_weather(api_key, city, units)
            if weather_info:
                display_weather_info(weather_info, city, units)
            else:
                st.error("City not found or an error occurred. Please check the city name and try again.")
        else:
            st.warning("Please enter a city name.")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
