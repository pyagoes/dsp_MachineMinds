from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import pandas as pd

# initiate FastAPI
app = FastAPI(description = "Telco-Customer-churn-API", version = "0.1")

# configure the db connection and session
engine = create_engine('postgresql://MachineMinds:MachineMinds@localhost:5432/customer_churn')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the table schema to store data
class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    customer_id = Column(String)
    gender = Column(String)
    senior_citizen = Column(Integer)
    partner = Column(String)
    dependents = Column(String)
    tenure = Column(Integer)
    phone_service = Column(String)
    multiple_lines = Column(String)
    internet_service = Column(String)
    online_security = Column(String)
    online_backup = Column(String)
    device_protection = Column(String)
    tech_support = Column(String)
    streaming_tv = Column(String)
    streaming_movies = Column(String)
    contract = Column(String)
    paperless_billing = Column(String)
    payment_method = Column(String)
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    prediction_date = Column(DateTime)
    source = Column(String)
    prediction = Column(Float)
    
# On-demand prediction endpoint
# list of objects, not only one row
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

<<<<<<< HEAD
@app.post("/predict/")
# change name
async def make_predictions(source: str, features: ModelFeatures):
    # get_pre is the model 
    predictions = 42
    prediction_date = datetime.utcnow()
    source = source
    feature1 = features.feature1
    feature2 = features.feature2
    feature3 = features.feature3
    feature4 = features.feature4
    feature5 = features.feature5
    prediction = 42
    prediction_db = Prediction(
        feature1 = feature1,
        feature2 = feature2,
        feature3 = feature3,
        feature4 = feature4,
        feature5 = feature5,
        prediction_date = prediction_date,
        source = source,
        prediction = prediction
        )
=======

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
    raw_df["PredictionDate"] = datetime.utcnow()
    raw_df["Source"] = source
    raw_df["Prediction"] = prediction_result
>>>>>>> 4d02abb0daff5f1f50439e4679becfbac62b25ec
    session = Session()
    for _,row in raw_df.iterrows():   
        prediction_db = Prediction(customer_id = row["customerID"], gender = row["gender"], 
                                senior_citizen = row["SeniorCitizen"], partner = row["Partner"],
                                dependents = row["Dependents"], tenure = row["tenure"],
                                phone_service = row["PhoneService"], multiple_lines = row["MultipleLines"],
                                internet_service = row["InternetService"], online_security = row["OnlineSecurity"],
                                online_backup = row["OnlineBackup"], device_protection = row["DeviceProtection"],
                                tech_support = row["TechSupport"], streaming_tv = row["StreamingTV"],
                                streaming_movies = row["StreamingMovies"], contract = row["Contract"],
                                paperless_billing = row["PaperlessBilling"], payment_method = row["PaymentMethod"],
                                monthly_charges = row["MonthlyCharges"], total_charges = row["TotalCharges"],
                                prediction_date = row["PredictionDate"], source = row["Source"], 
                                prediction = row["Prediction"]
                                )
    
        session.add(prediction_db)
        session.commit()
    session.close()
<<<<<<< HEAD
    # add save to db 
    return 42

# create the save to db enpoint
# add source in predict 
# refactor !!
#@app.post("/save/{source}")
# async def save_data(source : str, features : ModelFeatures):
#     prediction_date = datetime.utcnow()
#     source = source
#     feature1 = features.feature1
#     feature2 = features.feature2
#     feature3 = features.feature3
#     feature4 = features.feature4
#     feature5 = features.feature5
#     prediction = 42
#     prediction_db = Prediction(
#         feature1 = feature1,
#         feature2 = feature2,
#         feature3 = feature3,
#         feature4 = feature4,
#         feature5 = feature5,
#         prediction_date = prediction_date,
#         source = source,
#         prediction = prediction
#         )
#     session = Session()
#     session.add(prediction_db)
#     session.commit()
#     session.close()
#     return "the data is saved in the db" 


# Save model predictions, used features, prediction date and source in the database

# Define the table schema to store data
class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    feature1 = Column(Float)
    feature2 = Column(Float)
    feature3 = Column(Float)
    feature4 = Column(Float)
    feature5 = Column(Float)
    prediction_date = Column(DateTime)
    source = Column(String)
    prediction = Column(Float) 



# query the database for past prediction
=======
>>>>>>> 4d02abb0daff5f1f50439e4679becfbac62b25ec

# Define a function to convert a Prediction object to a dictionary
def prediction_to_dict(prediction):
    return {'monthly_charges' : prediction.monthly_charges, 'total_charges' : prediction.total_charges,
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
                                                            Prediction.prediction_date < end_datetime + timedelta(days = 1),
                                                            Prediction.source == prediction_source).all()
    else:
        past_predictions = session.query(Prediction).filter(Prediction.prediction_date >= start_datetime, 
                                                            Prediction.prediction_date < end_datetime + timedelta(days = 1)).all()

    past_predictions_dicts = [prediction_to_dict(prediction) for prediction in past_predictions]
    session.close()
    # filter on the source 
    return {'past_predictions': past_predictions_dicts}

