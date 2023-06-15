from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

default_args = {
    'owner': 'MachineMinds',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 15),  # Set a fixed date and time in the past
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'customer_churn_predictions',
    default_args=default_args,
    description='Scheduled customer churn predictions',
    schedule_interval=None,  # Disable automatic scheduling
)

def fetch_data():
    # Fetch data from the files, great expectations 
    # Store the retrieved data in a Pandas DataFrame or any appropriate data structure
    data = pd.read_csv("/Users/paulayagoesparza/Documents/S2/DSP/LOCAL/data_validation/good_quality_data/part1.csv", sep=',')
    return data


def make_predictions():
    data = fetch_data()

    # Define the feature values
    # Define the feature values
    features = {
        "SeniorCitizen": data["SeniorCitizen"].values.tolist(),
        "tenure": data["tenure"].values.tolist(),
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
        print('error')
        pass

predict_task = PythonOperator(
    task_id='make_predictions_task',
    python_callable=make_predictions,
    dag=dag
)


