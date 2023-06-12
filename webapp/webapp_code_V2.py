import json
import pandas as pd
import requests
import streamlit as st

def on_demand_predict():
    # Title
    st.title("On Demand Predictions WebApp")

    # Form to enter the variables by the user 
    with st.form("Single Sample Prediction"):
        # Let's try first with 3 features 
        senior_citizen = st.number_input("SeniorCitizen", value=0.0)
        tenure = st.number_input("Tenure", value=0.0)
        monthly_charges = st.number_input("MonthlyCharges", value=0.0)
        total_charges = st.number_input("TotalCharges", value=0.0)
        

        # Predict button for form
        predict_button = st.form_submit_button("Predict")

    # Add file uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    # Submit button for file upload
    predict_csv_button = st.button("Predict CSV")

    # Trigger API request on submit or file upload
    if predict_button:
        # Define the feature values
        features = {
            "customerID": "",
            "gender": "",
            "SeniorCitizen": senior_citizen,
            "Partner": "",
            "Dependents": "",
            "tenure": tenure,
            "PhoneService" : "",
            "MultipleLines" : "",
            "InternetService" : "",
            "OnlineSecurity" : "",
            "OnlineBackup" : "",
            "DeviceProtection" : "",
            "TechSupport" : "",
            "StreamingTV" : "",
            "StreamingMovies" : "",
            "Contract" : "",
            "PaperlessBilling" : "",
            "PaymentMethod" : "",
            "MonthlyCharges" : monthly_charges,
            "TotalCharges" : total_charges
            
        }
            

        # Send a POST request to the API endpoint with the feature values
        response = requests.post("http://127.0.0.1:8000/predict/webapp", json=features)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response data
            prediction = pd.DataFrame(response.json())
            # Display the prediction to the user
            st.write(prediction)
        else:
            # Handle the error
            st.write("Error: Failed to get prediction from the API endpoint.")

    if uploaded_file is not None and predict_csv_button:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file, header=0)

        #convert the numpy datatype to a native python type(int.64 --> int) because fastapi don't recognize them
        
        # Transform it into a dict
        features = df.to_dict(orient="records")
        

        # Send a POST request to the API endpoint with the feature values
        response = requests.post("http://127.0.0.1:8000/predict/webapp", json=features)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response data
            prediction = pd.DataFrame(response.json())
            # Display the prediction to the user
            st.write(prediction)
        else:
            # Handle the error
            st.write("Error: Failed to get prediction from the API endpoint.")


def past_predict():
    # Title
    st.title("Past Predictions WebApp")

    # Explanation of the WebApp
    #st.markdown("<h4 style='font-size:1.1em'>In this WebApp you can get predictions by selecting a date range and choosing one of the options of the drop list: 'webapp', 'scheduled predictions', 'all'</h4>", unsafe_allow_html=True)

    # Date selection component
    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")

    # Prediction source set list
    prediction_source = st.selectbox("Prediction source", ["webapp", "scheduled predictions", "all"])

    # Trigger API request on submit
    if st.button("Get Predictions"):
        with st.spinner('Loading predictions...'):
        # Define the request parameters
            params = {"start_date": start_date, "end_date": end_date, "prediction_source": prediction_source}

            # Send a GET request to the API endpoint with the parameters
            response = requests.get("http://127.0.0.1:8000/past-predictions", params=params)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the response data
                past_predictions = response.json()["past_predictions"]

                # Display an error message if there are no predictions for the desire date or source
                if len(past_predictions) == 0:
                    st.write("No predictions found for the selected date range and source.")
                else:
                    st.write("Past Predictions:")
                    st.write(pd.DataFrame(past_predictions))
            else:
                # Handle the error
                st.write("Error occurred: {}".format(response.text))


page_names_to_funcs = {
    "On Demand Predictions": on_demand_predict,
    "Past Predcitions": past_predict,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()



