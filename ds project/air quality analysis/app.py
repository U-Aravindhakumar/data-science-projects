import tkinter as tk
from tkinter import ttk
import pandas as pd
import pickle  # For loading the trained model

# Load your trained model and data
model = pickle.load(open('aqi_model.pkl', 'rb'))
data = pd.read_csv('processed_aqi_data.csv')  # Preprocessed dataset

# Function to predict AQI
def predict_aqi():
    year = int(year_var.get())
    location = location_var.get()
    
    # Filter the dataset for the selected year and location
    filtered_data = data[(data['Year'] == year) & (data['Location'] == location)]
    
    if not filtered_data.empty:
        # Use the trained model to predict AQI
        input_features = filtered_data[['SO2', 'NO2', 'PM10', 'PM2.5']].mean(axis=0).values.reshape(1, -1)
        aqi_category = model.predict(input_features)[0]
        result_label.config(text=f"Predicted AQI Category: {aqi_category}")
    else:
        result_label.config(text="No data available for the selected year and location")

# Create the GUI window
root = tk.Tk()
root.title("AQI Prediction System")

# Dropdown for Year
tk.Label(root, text="Select Year:").grid(row=0, column=0, padx=10, pady=10)
year_var = tk.StringVar()
year_dropdown = ttk.Combobox(root, textvariable=year_var, values=sorted(data['Year'].unique()))
year_dropdown.grid(row=0, column=1, padx=10, pady=10)

# Dropdown for Location
tk.Label(root, text="Select Location:").grid(row=1, column=0, padx=10, pady=10)
location_var = tk.StringVar()
location_dropdown = ttk.Combobox(root, textvariable=location_var, values=sorted(data['Location'].unique()))
location_dropdown.grid(row=1, column=1, padx=10, pady=10)

# Predict Button
predict_button = tk.Button(root, text="Predict AQI", command=predict_aqi)
predict_button.grid(row=2, column=0, columnspan=2, pady=20)

# Result Label
result_label = tk.Label(root, text="Predicted AQI Category will be displayed here")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
