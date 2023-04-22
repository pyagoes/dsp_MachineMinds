from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd


# initiate FastAPI
app = FastAPI(description = "Telco-Customer-churn-API", version = "0.1")

# configure the db connection and session
engine = create_engine('postgresql://paulayagoesparza:password@localhost:5432/customer_churn')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the table schema to store data
class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    customer_id: Column(String)
    gender: Column(String)
    senior_citizen: Column(Integer)
    partner: Column(String)
    dependents: Column(String)
    tenure: Column(Integer)
    phone_service: Column(String)
    multiple_lines: Column(String)
    internet_service: Column(String)
    online_security: Column(String)
    online_backup: Column(String)
    device_protection: Column(String)
    tech_support: Column(String)
    streaming_tv: Column(String)
    streaming_movies: Column(String)
    contract: Column(String)
    paperless_billing: Column(String)
    payment_method: Column(String)
    monthly_charges: Column(Float)
    total_charges: Column(Float)
    prediction_date = Column(DateTime)
    source = Column(String)
    prediction = Column(Float)
    
# On-demand prediction endpoint

class ModelFeatures(BaseModel):
    customerID: object = None
    gender: object = None
    SeniorCitizen: int = None
    Partner: object = None
    Dependents: object = None
    tenure: int = None
    PhoneService: object = None
    MultipleLines: object = None
    InternetService: object = None
    OnlineSecurity: object = None
    OnlineBackup: object = None
    DeviceProtection: object = None
    TechSupport: object = None
    StreamingTV: object = None
    StreamingMovies: object = None
    Contract: object = None
    PaperlessBilling: object = None
    PaymentMethod: object = None
    MonthlyCharges: float = None
    TotalCharges: float = None


@app.post("/predict/{source}")
async def make_predictions(features: Union[ModelFeatures, list], source : str):
    if isinstance(features,ModelFeatures):
        raw_df = pd.DataFrame.from_dict(features.dict(), orient="index").T
        prediction_df = raw_df.loc[:, ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]]
        prediction_result = 42.0
        prediction_df["prediction"] = prediction_result
    if isinstance(features, list):
        raw_df = pd.DataFrame(features)
        prediction_df = raw_df.copy()
        # Convert int columns to float beacuse FastAPI uses JSON format to serialize and deserialize data, and JSON does not have a native integer data type. Instead, JSON numbers are represented as either floating-point numbers or strings
        prediction_df["tenure"] = prediction_df["tenure"].astype(float)
        prediction_df["SeniorCitizen"] = prediction_df["SeniorCitizen"].astype(float)
        # Slice the prediction_df  
        prediction_df = prediction_df.loc[:, ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]]
        # add column predictions
        prediction_result = 42.0 #this value will be replaced after by our model result
        prediction_df["predictions"] = prediction_result

    # Save model predictions, used features, prediction date and source in the database
    save_to_db(source, raw_df, prediction_result)

    return prediction_df

def save_to_db(source, raw_df, prediction_result):
    prediction_db = Prediction(customer_id = raw_df["customerID"], gender = raw_df["genre"], 
                                senior_citizen = raw_df["SeniorCitizen"], partner = raw_df["Partner"],
                                dependents = raw_df["Dependents"], tenure = raw_df["tenure"],
                                phone_service = raw_df["PhoneService"], multiple_lines = raw_df["MultipleLines"],
                                internet_service = raw_df["InternetService"], online_security = raw_df["OnlineSecurity"],
                                online_backup = raw_df["OnlineBackup"], device_protection = raw_df["DeviceProtection"],
                                tech_support = raw_df["TechSupport"], streaming_tv = raw_df["StreamingTV"],
                                streaming_movies = raw_df["StreamingMovies"], contract = raw_df["Contract"],
                                paperless_billing = raw_df["PaperlessBilling"], payment_method = raw_df["PaymentMethod"],
                                monthly_charges = raw_df["MonthlyCharges"], total_charges = raw_df["TotalCharges"],
                                prediction_date = datetime.utcnow(), source = source, prediction = prediction_result
                                )
    session = Session()
    session.add(prediction_db)
    session.commit()
    session.close()

# Define a function to convert a Prediction object to a dictionary
def prediction_to_dict(prediction):
    return {'senior_citizen' : prediction.senior_citizen, 'tenure' : prediction.tenure,
            'monthly_charges' : prediction.monthly_charges, 'total_charges' : prediction.total_charges,
            'prediction_date': prediction.prediction_date, 'source': prediction.source, 
            'prediction': prediction.prediction
            }

# create the past-predictions endpoint
@app.get("/past-predictions/")
async def get_past_predictions(start_date : str, end_date : str, prediction_source : str):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    session = Session()
    if prediction_source != "all":
        past_predictions = session.query(Prediction).filter(Prediction.prediction_date >= start_datetime, 
                                                            Prediction.prediction_date <= end_datetime,
                                                            Prediction.source == prediction_source).all()
    else:
        past_predictions = session.query(Prediction).filter(Prediction.prediction_date >= start_datetime, 
                                                            Prediction.prediction_date <= end_datetime).all()

    past_predictions_dicts = [prediction_to_dict(prediction) for prediction in past_predictions]
    session.close()
    return {'past_predictions': past_predictions_dicts}
