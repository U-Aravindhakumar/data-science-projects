import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Load the trained model
model = joblib.load('outbreak_predictor_model.pkl')

def predict_outbreak(temperature, population_density, vaccination_rate):
    # Input preprocessing (same as training data)
    input_data = np.array([[temperature, population_density, vaccination_rate]])

    # Since the model was trained on scaled data, we also need to scale user inputs
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(input_data)
    
    # Make prediction
    prediction = model.predict(input_data_scaled)[0]
    probability = model.predict_proba(input_data_scaled)[0][1]  # Probability of outbreak

    result = 'Outbreak' if prediction == 1 else 'No Outbreak'
    return result, probability * 100

# Function to get user input
def get_user_input():
    try:
        temperature = float(input("Enter the temperature (°C): "))
        population_density = float(input("Enter the population density (people per sq km): "))
        vaccination_rate = float(input("Enter the vaccination rate (%): "))
        
        if not (0 <= vaccination_rate <= 100):
            raise ValueError("Vaccination rate must be between 0 and 100.")
        
        return temperature, population_density, vaccination_rate
    
    except ValueError as ve:
        print(f"Invalid input: {ve}")
        return None

# Main logic
user_input = get_user_input()
if user_input:
    temperature, population_density, vaccination_rate = user_input
    result, probability = predict_outbreak(temperature, population_density, vaccination_rate)
    print(f"Prediction: {result}, Probability: {probability:.2f}%")
