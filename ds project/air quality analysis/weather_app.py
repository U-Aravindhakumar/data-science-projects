# import tkinter as tk
# from tkinter import messagebox
# import requests

# # Function to get the weather and air quality data
# def get_data():
#     city = city_entry.get()
#     if city == "":
#         messagebox.showerror("Error", "Please enter a city name")
#         return

#     # WeatherAPI URL (replace with your own API key)
#     weather_api_key = "193dace6d87141fb8b743845242409"
#     weather_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=yes"

#     try:
#         # Fetch weather data
#         weather_response = requests.get(weather_url)
#         weather_data = weather_response.json()

#         if "error" in weather_data:
#             messagebox.showerror("Error", "City not found!")
#             return

#         temp = weather_data["current"]["temp_c"]
#         weather_description = weather_data["current"]["condition"]["text"]
#         air_quality = weather_data["current"]["air_quality"]["us-epa-index"]

#         # Display the results
#         result_label.config(text=f"City: {city}\nTemperature: {temp}°C\nWeather: {weather_description}\nAir Quality Index (AQI): {air_quality}")
#     except requests.exceptions.RequestException as e:
#         messagebox.showerror("Error", "Failed to retrieve data. Please check your internet connection.")

# # Create the main window
# root = tk.Tk()
# root.title("Air Quality and Temperature Monitoring System")

# # Create and place the labels, entry widgets, and button
# city_label = tk.Label(root, text="Enter City:")
# city_label.pack(pady=5)

# city_entry = tk.Entry(root, width=30)
# city_entry.pack(pady=5)

# get_data_button = tk.Button(root, text="Get Data", command=get_data)
# get_data_button.pack(pady=10)

# result_label = tk.Label(root, text="", font=("Helvetica", 12))
# result_label.pack(pady=20)

# # Run the main loop
# root.mainloop()







import requests
import pandas as pd
import joblib
import streamlit as st

# Fetch recent data
def fetch_recent_data(city, days=3):
    API_KEY = "193dace6d87141fb8b743845242409"
    data = []
    for i in range(days):
        date = (pd.Timestamp.now() - pd.Timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={date}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            day_data = weather_data["forecast"]["forecastday"][0]["day"]
            air_quality = weather_data["current"]["air_quality"]
            data.append({
                "temp": day_data["avgtemp_c"],
                "humidity": day_data["avghumidity"],
                "wind_speed": day_data["maxwind_kph"],
                "aqi": air_quality["us-epa-index"]
            })
        else:
            print(f"Failed to fetch data for {date}")
    return pd.DataFrame(data)

# Predict AQI
def predict_aqi(data):
    model = joblib.load("air_quality_model.pkl")
    predictions = model.predict(data[["temp", "humidity", "wind_speed"]])
    data["predicted_aqi"] = predictions
    return data

# Streamlit GUI
st.title("Real-Time Air Quality Prediction")

city_input = st.text_input("Enter city name:", value="Chennai")

if st.button("Fetch and Predict"):
    try:
        # Fetch recent data
        recent_data = fetch_recent_data(city_input, days=3)
        
        # Predict AQI
        predicted_data = predict_aqi(recent_data)
        
        # Display predictions
        st.write(f"### Recent Air Quality Predictions for {city_input}")
        st.dataframe(predicted_data)
    except Exception as e:
        st.error(f"Error: {e}")
