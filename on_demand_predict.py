import streamlit as st
import pandas as pd
import requests

# Title
st.title("OnDemand Predictions WebApp")

# Form to enter the variables by the user 
with st.form("Single Sample Prediction"):
    # Let's try first with 3 features 
    feature1 = st.number_input("Feature 1", value=0.0)
    feature2 = st.number_input("Feature 2", value=0.0)
    feature3 = st.number_input("Feature 3", value=0.0)
    feature4 = st.number_input("Feature 4", value=0.0)
    feature5 = st.number_input("Feature 5", value=0.0)

    # Submit button
    submit_button = st.form_submit_button("Predict")

# Add file uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Trigger API request on submit or file upload
# Option 1: the users enters values manually
if submit_button:
    # Option 2: the user uploads a CSV	
    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file, header=0)
        # Transform it into a dict
        features = df.to_dict(orient="records")[0]
        
    else:
        # Define the feature values
        features = {
            "feature1": feature1,
            "feature2": feature2,
            "feature3": feature3,
            "feature4": feature4,
            "feature5": feature5
        }
     
     # Send a POST request to the API endpoint with the feature values
    response = requests.post("http://127.0.0.1:8070/predict", json=features)
        
    # Call the endpoint in the API to save predictions 
    # Send a POST request to the save endpoint with the feature values and source
    save_response = requests.post(f"http://127.0.0.1:8070/save/webapp", json=features)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response data
        prediction = response.json()
        # Display the prediction to the user
        st.write("Prediction:", prediction)
    else:
        # Handle the error
        st.write("Error: Failed to get prediction from the API endpoint.")



