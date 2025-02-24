import requests
import pandas as pd
import joblib

# Replace with your API key
API_KEY = "193dace6d87141fb8b743845242409"

# Function to fetch real-time data
def fetch_city_data(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        air_quality = data['current']['air_quality']['us-epa-index']
        return {"temp": temp, "humidity": humidity, "wind_speed": wind_speed, "air_quality": air_quality}
    else:
        raise ValueError("Error fetching data. Check your city name or API key.")

# Function to predict AQI
def predict_aqi(data):
    model = joblib.load("air_quality_model.pkl")
    input_data = pd.DataFrame([data], columns=["temp", "humidity", "wind_speed"])
    predicted_aqi = model.predict(input_data)[0]
    return predicted_aqi
