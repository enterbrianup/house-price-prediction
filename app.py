from fastapi import FastAPI
from typing import Annotated
import pandas as pd
from pydantic import BaseModel, Field
import joblib


app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
# Load model
with open("housing_model.pkl", "rb") as f:
    model = joblib.load(f)

# Input validation model
class UserInput(BaseModel):
    bedrooms: Annotated[int, Field(..., gt=0, lt=15, description="Number of bedrooms")]
    bathrooms: Annotated[float, Field(..., gt=0, lt=10, description="Number of bathrooms")]
    sqft_living: Annotated[float, Field(..., gt=200, lt=20000, description="Living area in square feet")]
    sqft_lot: Annotated[float, Field(..., gt=200, lt=1000000, description="Lot size in square feet")]
    floors: Annotated[float, Field(..., gt=0, lt=5, description="Number of floors")]
    waterfront: Annotated[int, Field(..., ge=0, le=1, description="1 if waterfront, else 0")]
    view: Annotated[int, Field(..., ge=0, le=4, description="Quality of view (0–4)")]
    condition: Annotated[int, Field(..., ge=1, le=5, description="Condition rating (1–5)")]
    grade: Annotated[int, Field(..., ge=1, le=13, description="Grade rating (1–13)")]
    sqft_above: Annotated[float, Field(..., gt=200, lt=20000, description="Square feet above ground")]
    sqft_basement: Annotated[float, Field(..., ge=0, lt=10000, description="Square feet basement")]
    yr_built: Annotated[int, Field(..., ge=1800, le=2025, description="Year built")]
    yr_renovated: Annotated[int, Field(..., ge=0, le=2025, description="Year renovated (0 if never)")]
    zipcode: Annotated[int, Field(..., ge=98001, le=98199, description="Zipcode of the house")]
    lat: Annotated[float, Field(..., gt=47.0, lt=48.0, description="Latitude")]
    long: Annotated[float, Field(..., gt=-123.0, lt=-121.0, description="Longitude")]
    sqft_living15: Annotated[float, Field(..., gt=200, lt=20000, description="Living room area of 15 nearest neighbors")]
    sqft_lot15: Annotated[float, Field(..., gt=200, lt=1000000, description="Lot size of 15 nearest neighbors")]


@app.post("/predict")
def predict(data: UserInput):
    # Convert input to DataFrame
    df = pd.DataFrame([data.model_dump()])  # safer than using .values() and .keys()

    # Make prediction
    prediction = model.predict(df)

    # Return JSON-safe output
    return {"predicted_price": float(prediction[0])}
