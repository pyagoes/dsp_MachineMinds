# Telco Churn Prediction Application

This project is aimed at predicting customer churn for a telco company using machine learning techniques. The project implements an ML-powered application consisting of various components and technologies.

## Project Components

1. **User Interface (UI):** The user interface allows users to make on-demand predictions by either typing the feature values or uploading a CSV file. Users can also view past predictions through the interface. The UI is implemented using Streamlit, a Python library for building interactive web applications.

2. **API (Application Programming Interface):** The ML model is exposed through an API built with FastAPI, a modern, fast (high-performance) web framework for building APIs with Python. The API has two endpoints: one for making predictions and another for saving the predictions to a database. The ML model is loaded using joblib, a library for serializing Python objects.

3. **Database:** Predictions and associated data, such as the used feature values, are stored in a PostgreSQL database. PostgreSQL is a powerful, open-source relational database management system.

4. **Prediction Job:** Scheduled predictions are made every 5 minutes using an Apache Airflow DAG (Directed Acyclic Graph). The DAG reads data files from a high-quality data folder, calls the API to make predictions, and saves the predictions to the database.

5. **Ingestion Job:** Data quality and validation are performed using Great Expectations, a library that checks for missing values, data types, and other criteria. An Airflow DAG executes the data validation process every 5 minutes to ensure the integrity of the ingested data.

6. **Monitoring Dashboard:** A Grafana-based monitoring dashboard is provided to monitor the quality of ingested data and track the drift between training and serving data. Grafana is an open-source analytics and monitoring solution that allows for the creation of customizable dashboards.

## Setup and Installation

To set up and run the Telco Churn Prediction Application, follow these steps:

1. Clone the project repository from [GitHub link](https://github.com/pyagoes/dsp_MachineMinds.git).

2. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database and configure the database connection parameters in the project settings.

4. Set up Apache Airflow.

5. Configure the Great Expectations environment.

6. Install Grafana and set up the monitoring dashboard, connecting it to the necessary data sources.


## Usage

1. Access the Streamlit UI by opening a web browser and navigating to the appropriate URL.

2. Use the UI to input feature values manually or upload a CSV file containing the feature data.

3. Click the "Predict" button to make a churn prediction based on the provided input.

4. View past predictions by selecting the appropriate option in the UI.

5. Monitor the data quality and validation results through the Grafana monitoring dashboard.


```python

```
