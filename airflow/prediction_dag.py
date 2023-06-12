from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

default_args = {
    'owner': 'MachineMinds',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'customer_churn_predictions',
    default_args=default_args,
    description='Scheduled customer churn predictions',
    schedule_interval=timedelta(minutes=5)
)

def fetch_data():
    # Fetch data from the files, great expectations 
    # Store the retrieved data in a Pandas DataFrame or any appropriate data structure
    data = pd.read_csv("/Users/paulayagoesparza/Documents/GitHub/try.csv", sep=';')  
    return data


def make_predictions():
    data = fetch_data()

    # Define the feature values
    features = {
        "customerID": data["customerID"].values.tolist(),
        "gender": data["gender"].values.tolist(),
        "SeniorCitizen": data["SeniorCitizen"].values.tolist(),
        "Partner": data["Partner"].values.tolist(),
        "Dependents": data["Dependents"].values.tolist(),
        "tenure": data["tenure"].values.tolist(),
        "PhoneService": data["PhoneService"].values.tolist(),
        "MultipleLines": data["MultipleLines"].values.tolist(),
        "InternetService": data["InternetService"].values.tolist(),
        "OnlineSecurity": data["OnlineSecurity"].values.tolist(),
        "OnlineBackup": data["OnlineBackup"].values.tolist(),
        "DeviceProtection": data["DeviceProtection"].values.tolist(),
        "TechSupport": data["TechSupport"].values.tolist(),
        "StreamingTV": data["StreamingTV"].values.tolist(),
        "StreamingMovies": data["StreamingMovies"].values.tolist(),
        "Contract": data["Contract"].values.tolist(),
        "PaperlessBilling": data["PaperlessBilling"].values.tolist(),
        "PaymentMethod": data["PaymentMethod"].values.tolist(),
        "MonthlyCharges": data["MonthlyCharges"].values.tolist(),
        "TotalCharges": data["TotalCharges"].values.tolist()
    }

    # Send a POST request to the API endpoint with the feature values
    response = requests.post("http://127.0.0.1:8000/predict/scheduled", json=features)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response data
        prediction = pd.DataFrame(response.json())
        # Do any further processing or save the prediction if needed
    else:
        # Handle the error
        pass

predict_task = PythonOperator(
    task_id='make_predictions_task',
    python_callable=make_predictions,
    dag=dag
)


