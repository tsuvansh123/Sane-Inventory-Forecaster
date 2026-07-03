from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import joblib
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

# ── Load .env file ─────────────────────────────────────────────────────────
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    item_id: int
    current_stock: int
    lead_time_days: int
    day_of_week: int
    month: int
    day_of_year: int
    week_of_year: int
    lag_7: float
    lag_14: float
    lag_30: float
    rolling_mean_7: float
    rolling_mean_30: float

# 4. Define the data structure for the login request
class LoginCredentials(BaseModel):
    username: str
    password: str

# 5. Define the data structure for the AI chat endpoint
class QueryRequest(BaseModel):
    question: str
    forecast_data: List[Any]

@app.get("/")
def read_root():
    return {"status": "API is live and ready."}

# 6. The secure login endpoint
@app.post("/login")
def login(credentials: LoginCredentials):
    if credentials.username == "admin" and credentials.password == "admin123":
        return {
            "status": "success",
            "message": "Authentication successful",
            "token": "wfx-auth-token-789"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# 7. The core prediction endpoint
@app.post("/predict")
def predict_demand(data: SkuData):
    if model is None:
        return {"error": "Machine learning model is not loaded."}

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

    prediction = model.predict(input_df)[0]

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

# 8. AI chat endpoint — powered by Groq + LLaMA 3.1
@app.post("/query")
def query_forecast(request: QueryRequest):
    """
    Receives the user's plain-English question + the /predict results,
    passes both to LLaMA 3.1 via Groq, returns a plain-English answer.
    """
    if not request.forecast_data:
        raise HTTPException(status_code=400, detail="No forecast data provided.")

    df = pd.DataFrame(request.forecast_data)
    forecast_table = df.to_string(index=False)

    prompt = f"""You are a senior inventory analyst for an apparel supply chain company called SANE.

You have been given the following XGBoost demand forecast results:

{forecast_table}

Columns explained:
- item_id: the SKU number
- predicted_30_day_demand: units expected to be sold in next 30 days
- current_stock: units currently in the warehouse
- suggested_reorder_quantity: how many units to order now (0 = no action needed)
- inventory_status: "Stockout Risk High" means urgent reorder needed

A business user has asked:
"{request.question}"

Instructions:
- Answer in plain English — no jargon, no code, no markdown formatting.
- Be specific: reference actual item_id numbers and quantities from the data above.
- If the question is about risk, list the top 3 highest-risk SKUs by item_id.
- If you cannot answer from the data alone, say so clearly.
- Keep your answer under 180 words.
- End with one short actionable recommendation if relevant."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq error: {str(e)}")