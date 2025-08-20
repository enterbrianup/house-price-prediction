import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/predict"

st.title("🏡 House Price Prediction")

# Create input form
with st.form("prediction_form"):
    bedrooms = st.number_input("Number of bedrooms", min_value=1, max_value=15, value=3)
    bathrooms = st.number_input("Number of bathrooms", min_value=1.0, max_value=10.0, value=2.0, step=0.5)
    sqft_living = st.number_input("Living area (sqft)", min_value=200, max_value=20000, value=1800)
    sqft_lot = st.number_input("Lot size (sqft)", min_value=200, max_value=1000000, value=5000)
    floors = st.number_input("Number of floors", min_value=1.0, max_value=5.0, value=1.0, step=0.5)
    waterfront = st.selectbox("Waterfront", [0, 1])
    view = st.slider("View quality (0–4)", 0, 4, 0)
    condition = st.slider("Condition (1–5)", 1, 5, 3)
    grade = st.slider("Grade (1–13)", 1, 13, 7)
    sqft_above = st.number_input("Above ground area (sqft)", min_value=200, max_value=20000, value=1500)
    sqft_basement = st.number_input("Basement area (sqft)", min_value=0, max_value=10000, value=300)
    yr_built = st.number_input("Year built", min_value=1800, max_value=2025, value=1990)
    yr_renovated = st.number_input("Year renovated (0 if never)", min_value=0, max_value=2025, value=0)
    zipcode = st.number_input("Zipcode", min_value=98001, max_value=98199, value=98105)
    lat = st.number_input("Latitude", min_value=47.0, max_value=48.0, value=47.5, format="%.6f")
    long = st.number_input("Longitude", min_value=-123.0, max_value=-121.0, value=-122.2, format="%.6f")
    sqft_living15 = st.number_input("Living area of 15 neighbors (sqft)", min_value=200, max_value=20000, value=1800)
    sqft_lot15 = st.number_input("Lot size of 15 neighbors (sqft)", min_value=200, max_value=1000000, value=5000)

    submit = st.form_submit_button("Predict Price")

# When user submits
if submit:
    input_data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "sqft_lot": sqft_lot,
        "floors": floors,
        "waterfront": waterfront,
        "view": view,
        "condition": condition,
        "grade": grade,
        "sqft_above": sqft_above,
        "sqft_basement": sqft_basement,
        "yr_built": yr_built,
        "yr_renovated": yr_renovated,
        "zipcode": zipcode,
        "lat": lat,
        "long": long,
        "sqft_living15": sqft_living15,
        "sqft_lot15": sqft_lot15
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"💰 Predicted Price: ${result['predicted_price']:,.2f}")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
