import streamlit as st
import requests

# 1. Configure the page settings
st.set_page_config(page_title="WFX Inventory Dashboard", page_icon="📦", layout="wide")

st.title("📦 SANE Inventory Forecaster")
st.markdown("Predictive analytics dashboard for apparel supply chain optimization.")
st.markdown("---")

# 2. Build the Sidebar for User Inputs
st.sidebar.header("Warehouse Input Parameters")
item_id = st.sidebar.number_input("SKU / Item ID", value=101)
current_stock = st.sidebar.number_input("Current Stock Level", value=50)
lead_time_days = st.sidebar.number_input("Vendor Lead Time (Days)", value=14)

st.sidebar.markdown("---")
st.sidebar.subheader("Machine Learning Features")
st.sidebar.caption("Historical data fed to the XGBoost Engine")

day_of_week = st.sidebar.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 2)
month = st.sidebar.slider("Month (1-12)", 1, 12, 6)
day_of_year = st.sidebar.number_input("Day of Year", value=150)
week_of_year = st.sidebar.number_input("Week of Year", value=22)

lag_7 = st.sidebar.number_input("Sales 7 Days Ago", value=15.0)
lag_14 = st.sidebar.number_input("Sales 14 Days Ago", value=18.0)
lag_30 = st.sidebar.number_input("Sales 30 Days Ago", value=20.0)
rolling_mean_7 = st.sidebar.number_input("7-Day Moving Avg", value=16.5)
rolling_mean_30 = st.sidebar.number_input("30-Day Moving Avg", value=19.0)

# 3. Connect to the FastAPI Backend
if st.sidebar.button("Generate AI Forecast"):
    
    # Package the inputs exactly as FastAPI expects them
    payload = {
        "item_id": item_id,
        "current_stock": current_stock,
        "lead_time_days": lead_time_days,
        "day_of_week": day_of_week,
        "month": month,
        "day_of_year": day_of_year,
        "week_of_year": week_of_year,
        "lag_7": lag_7,
        "lag_14": lag_14,
        "lag_30": lag_30,
        "rolling_mean_7": rolling_mean_7,
        "rolling_mean_30": rolling_mean_30
    }

    # Display a loading spinner while waiting for the AI
    with st.spinner("Calculating AI predictions via FastAPI..."):
        try:
            # Send POST request to your local server
            # Send POST request to the Render server
            response = requests.post("https://sane-inventory-forecaster.onrender.com/predict", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # 4. Display the Results Beautifully
                st.subheader(f"Forecast Results for Item #{data['item_id']}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Predicted 30-Day Demand", value=data["predicted_30_day_demand"])
                col2.metric(label="Current Stock", value=data["current_stock"])
                col3.metric(label="Suggested Reorder Qty", value=data["suggested_reorder_quantity"])
                
                st.markdown("### Status Alert")
                if data["inventory_status"] == "Stockout Risk High":
                    st.error("🚨 CRITICAL: Stockout Risk High. Immediate reorder recommended to prevent supply chain disruption.")
                else:
                    st.success("✅ Stock Optimal. No immediate action required.")
            else:
                st.error(f"API Error: Received status code {response.status_code}")
                
        except Exception as e:
            st.error(f"Failed to connect to the FastAPI server. Make sure it is running in your other terminal! Error: {e}")