from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize the application
app = FastAPI(
    title="Intelligent Inventory Forecaster API",
    description="Predictive analytics engine for apparel supply chain optimization."
)

# 2. Load the trained machine learning model
try:
    model = joblib.load('inventory_model.pkl')
except FileNotFoundError:
    model = None
    print("Warning: Model file not found. Ensure the .pkl file is in the directory.")

# 3. Define the exact data structure the model expects
class SkuData(BaseModel):
    # Business logic fields (used by the API, but not sent to the ML model)
    item_id: int
    current_stock: int
    lead_time_days: int
    
    # Machine Learning fields (The exact 9 features XGBoost expects)
    day_of_week: int
    month: int
    day_of_year: int
    week_of_year: int
    lag_7: float
    lag_14: float
    lag_30: float
    rolling_mean_7: float
    rolling_mean_30: float

@app.get("/")
def read_root():
    return {"status": "API is live and ready."}

# 4. The core prediction endpoint
@app.post("/predict")
def predict_demand(data: SkuData):
    if model is None:
        return {"error": "Machine learning model is not loaded."}

    # Format the incoming data exactly with the 9 columns the model was trained on
    # Notice we DO NOT include 'item' or 'store' here anymore
    input_df = pd.DataFrame([{
        'day_of_week': data.day_of_week,
        'month': data.month,
        'day_of_year': data.day_of_year,
        'week_of_year': data.week_of_year,
        'lag_7': data.lag_7,
        'lag_14': data.lag_14,
        'lag_30': data.lag_30,
        'rolling_mean_7': data.rolling_mean_7,
        'rolling_mean_30': data.rolling_mean_30
    }])
    
    # Generate the prediction
    prediction = model.predict(input_df)[0]
    
    # Calculate reorder logic
    predicted_demand = max(0, int(prediction))
    reorder_point = predicted_demand * (data.lead_time_days / 30.0)
    suggested_order = max(0, int(reorder_point - data.current_stock))
    
    status = "Stockout Risk High" if suggested_order > 0 else "Stock Optimal"

    return {
        "item_id": data.item_id,
        "predicted_30_day_demand": predicted_demand,
        "current_stock": data.current_stock,
        "suggested_reorder_quantity": suggested_order,
        "inventory_status": status
    }