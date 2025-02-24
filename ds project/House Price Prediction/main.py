import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Create a sample dataset
def create_dataset(num_samples=1000):
    np.random.seed(0)  # For reproducibility

    sizes = np.random.randint(800, 5000, num_samples)  # Size in sq ft
    bedrooms = np.random.randint(1, 6, num_samples)  # Number of bedrooms
    locations = np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai'], num_samples)
    ages = np.random.randint(0, 30, num_samples)  # Age of the house in years
    prices = np.random.randint(2000000, 20000000, num_samples)  # Price in INR

    # Create a DataFrame
    data = pd.DataFrame({
        'Size': sizes,
        'Bedrooms': bedrooms,
        'Location': locations,
        'Age': ages,
        'Price': prices
    })

    return data

# Step 2: Prepare data and train model
def train_model(data):
    # One-hot encode categorical variables
    data = pd.get_dummies(data, columns=['Location'], drop_first=True)
    
    # Split data into features and target variable
    X = data.drop('Price', axis=1)
    y = data['Price']

    # Split into training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))
    
    return model, X.columns

# Step 3: Define prediction function
def predict_price(model, feature_names, size, bedrooms, age, location):
    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'Size': [size],
        'Bedrooms': [bedrooms],
        'Age': [age]
    })
    
    # One-hot encode the location
    location_dummies = pd.get_dummies([location], prefix='Location')
    
    # Ensure all location columns are present with a value of 0 if not found
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai']
    for loc in locations:
        loc_col = f'Location_{loc}'
        if loc_col not in location_dummies:
            location_dummies[loc_col] = 0

    # Concatenate the one-hot encoded location columns with the input data
    input_data = pd.concat([input_data, location_dummies], axis=1)
    
    # Reindex the input_data to have the same columns as the model
    input_data = input_data.reindex(columns=feature_names, fill_value=0)

    # Make prediction
    predicted_price = model.predict(input_data)
    return predicted_price[0]

# Main code execution
if __name__ == "__main__":
    # Create and train the model
    dataset = create_dataset()
    model, feature_names = train_model(dataset)

    # Prediction step (user input)
    size = int(input("Enter the size of the house (sq ft): "))
    bedrooms = int(input("Enter the number of bedrooms: "))
    age = int(input("Enter the age of the house (in years): "))
    location = input("Enter the location (e.g., Mumbai, Delhi, Bangalore, Chennai): ")

    predicted_price = predict_price(model, feature_names, size, bedrooms, age, location)
    print(f"Predicted price for the house: {predicted_price:.2f} INR")
