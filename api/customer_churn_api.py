from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# initiate FastAPI
app = FastAPI(description = "Telco-Customer-churn-API", version = "0.1")

# configure the db connection and session
engine = create_engine('postgresql://paulayagoesparza:password@localhost:5432/customer_churn')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# On-demand prediction endpoint

class ModelFeatures(BaseModel):
    feature1: float   
    feature2: float  
    feature3: float 
    feature4: float 
    feature5: float 

@app.post("/predict/")
async def make_predictions(features: ModelFeatures):
    return 42


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

# create the save to db enpoint
@app.post("/save/{source}")
async def save_data(source : str, features : ModelFeatures):
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
    session = Session()
    session.add(prediction_db)
    session.commit()
    session.close()
    return "the data is saved in the db" 

# query the database for past prediction

# Define a function to convert a Prediction object to a dictionary
def prediction_to_dict(prediction):
    return {'id': prediction.id, 'feature1': prediction.feature1, 'feature2': prediction.feature2, 
            'feature3': prediction.feature3, 'feature4': prediction.feature4, 'feature5': prediction.feature5,
            'prediction_date': prediction.prediction_date, 'source': prediction.source, 
            'prediction': prediction.prediction
            }

# create the past-predictions endpoint
@app.get("/past-predictions")
async def get_past_predictions(start_date : str, end_date : str):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    session = Session()
    past_predictions = session.query(Prediction).filter(Prediction.prediction_date >= start_datetime, Prediction.prediction_date <= end_datetime).all()
    past_predictions_dicts = [prediction_to_dict(prediction) for prediction in past_predictions]
    session.close()
    return {'past_predictions': past_predictions_dicts}
 
