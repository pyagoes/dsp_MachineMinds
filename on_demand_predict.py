import streamlit as st

# Title
st.title("OnDemand Predictions WebApp")
# Text
st.write("This is the WebApp for the user to make past predictions")

# Form for single sample prediction
with st.form("Single Sample Prediction"):
    # Let's try first with 3 features 
    feature1 = st.number_input("Feature 1", value=0.0)
    feature2 = st.number_input("Feature 2", value=0.0)
    feature3 = st.number_input("Feature 3", value=0.0)
    feature4 = st.number_input("Feature 4", value=0.0)
    feature5 = st.number_input("Feature 5", value=0.0)

    # Add submit button
    submit_button = st.form_submit_button("Predict")

# Add file uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Trigger API request on submit
if submit_button:
    # Call the API endpoint with the entered feature values
    # and process the prediction response
    # (e.g., display the predicted output to the user)
    prediction = make_prediction(feature1, feature2, feature3, feature4, feature5)
    st.write("Prediction:", prediction)

import requests

# Define the API endpoint URL
url = "http://127.0.0.1:8000/predict"

# Define the feature values
features = {
    "feature1": 0.5,
    "feature2": 1.0,
    "feature3": 0.8
}

# Send a POST request to the API endpoint with the feature values
response = requests.post(url, json=features)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response data
    prediction = response.json()["prediction"]
    # Display the prediction to the user
    print(f"Prediction: {prediction}")
else:
    # Handle the error
    print("Error: Failed to get prediction from the API endpoint.")


