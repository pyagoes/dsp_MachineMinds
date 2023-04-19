import streamlit as st
import pandas as pd
import requests

# Title
st.title("Past Predictions WebApp")

# Explanation of the WebApp 
st.markdown("<h4 style='font-size:1.1em'>In this WebApp you can get predictions by selecting a date range and choosing one of the options of the drop list: 'webapp', 'scheduled predictions', 'all'</h4>", unsafe_allow_html=True)

# Add file uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Date selection component
start_date = st.date_input("Start date")
end_date = st.date_input("End date")

# Prediction source set list 
prediction_source = st.selectbox("Prediction source", ["webapp", "scheduled predictions", "all"])

# Trigger API request on submit or file upload
if st.button("Get Predictions"):
    # Define the request parameters
    params = {"start_date": start_date, "end_date": end_date, "prediction_source": prediction_source}

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        # Send a POST request to the API endpoint with the DataFrame
        response = requests.post("http://127.0.0.1:8000/predict", json=df.to_json(orient="records"), params=params)
    else:
        # Send a GET request to the API endpoint with the parameters
        response = requests.get("http://127.0.0.1:8000/predict", params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response data
        predictions = response.json()["predictions"]
        # Display the predictions to the user
        st.write("Predictions:")
        st.write(pd.DataFrame(predictions))
    else:
        # Handle the error
        st.write("Error: Failed to get predictions from the API endpoint.")

