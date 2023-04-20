import streamlit as st
import pandas as pd
import requests

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
        response = requests.get("http://127.0.0.1:8070/past-predictions", params=params)

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

