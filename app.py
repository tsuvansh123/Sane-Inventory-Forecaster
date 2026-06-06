import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go # <-- New Plotly Import

# --- 1. Configure the page settings ---
st.set_page_config(page_title="WFX Inventory Dashboard", page_icon="📦", layout="wide")

# --- 2. Hide Streamlit Branding ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- 4. Login Page Function ---
def login_page():
    col1, col2, col3 = st.columns([1, 1, 1]) 
    with col2:
        st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📦 WFX Forecaster</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6B7280; margin-bottom: 20px;'>Enterprise Inventory Intelligence</p>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            st.markdown("### Secure Login")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.write("") 
            submit_button = st.form_submit_button("Sign In", use_container_width=True)

            if submit_button:
                with st.spinner("Authenticating..."):
                    try:
                        login_url = "https://sane-inventory-forecaster.onrender.com/login" 
                        payload = {"username": username, "password": password}
                        response = requests.post(login_url, json=payload)

                        if response.status_code == 200:
                            data = response.json()
                            if data.get("status") == "success":
                                st.session_state["logged_in"] = True
                                st.rerun()
                        elif response.status_code == 401:
                            st.error("Access Denied: Invalid credentials.")
                        else:
                            st.error(f"Server Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Failed to connect to backend server. Error: {e}")

# --- 5. Main Dashboard Function ---
def main_dashboard():
    with st.sidebar:
        st.markdown("### Account")
        if st.button("Sign Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
        st.markdown("---")
        
    st.title("📦 SANE Inventory Forecaster")
    st.markdown("Predictive analytics dashboard for apparel supply chain optimization.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Single Item Forecast", "Bulk CSV Upload"])

    # --- TAB 1: Single Item Logic ---
    with tab1:
        st.header("Manual Parameter Entry")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            item_id = st.number_input("SKU / Item ID", value=101)
            current_stock = st.number_input("Current Stock Level", value=50)
            lead_time_days = st.number_input("Vendor Lead Time (Days)", value=14)
        with col2:
            day_of_week = st.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 2)
            month = st.slider("Month (1-12)", 1, 12, 6)
            day_of_year = st.number_input("Day of Year", value=150)
            week_of_year = st.number_input("Week of Year", value=22)
        with col3:
            lag_7 = st.number_input("Sales 7 Days Ago", value=15.0)
            lag_14 = st.number_input("Sales 14 Days Ago", value=18.0)
            lag_30 = st.number_input("Sales 30 Days Ago", value=20.0)
            rolling_mean_7 = st.number_input("7-Day Moving Avg", value=16.5)
            rolling_mean_30 = st.number_input("30-Day Moving Avg", value=19.0)

        if st.button("Generate AI Forecast", type="primary"):
            payload = {
                "item_id": item_id, "current_stock": current_stock, "lead_time_days": lead_time_days,
                "day_of_week": day_of_week, "month": month, "day_of_year": day_of_year,
                "week_of_year": week_of_year, "lag_7": lag_7, "lag_14": lag_14,
                "lag_30": lag_30, "rolling_mean_7": rolling_mean_7, "rolling_mean_30": rolling_mean_30
            }

            with st.spinner("Calculating AI predictions via FastAPI..."):
                try:
                    response = requests.post("https://sane-inventory-forecaster.onrender.com/predict", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.subheader(f"Forecast Results for Item #{data['item_id']}")
                        
                        res_col1, res_col2, res_col3 = st.columns(3)
                        res_col1.metric(label="Predicted 30-Day Demand", value=data["predicted_30_day_demand"])
                        res_col2.metric(label="Current Stock", value=data["current_stock"])
                        res_col3.metric(label="Suggested Reorder Qty", value=data["suggested_reorder_quantity"])
                        
                        # --- NEW PLOTLY CHART VISUALIZATION ---
                        st.markdown("### Demand Trend Analysis")
                        
                        # Create x-axis labels
                        days = ["30 Days Ago", "14 Days Ago", "7 Days Ago", "Today", "Predicted (Next 30 Days)"]
                        # Create y-axis data combining historical inputs and the AI prediction
                        sales_trend = [lag_30, lag_14, lag_7, rolling_mean_7, data["predicted_30_day_demand"]]
                        
                        # Build the high-contrast chart
                        fig = go.Figure()
                        
                        # Historical Data Line
                        fig.add_trace(go.Scatter(
                            x=days[:4], y=sales_trend[:4],
                            mode='lines+markers',
                            name='Historical Sales',
                            line=dict(color='#6B7280', width=3),
                            marker=dict(size=8)
                        ))
                        
                        # AI Prediction Line (Bright highlight color)
                        fig.add_trace(go.Scatter(
                            x=days[3:], y=sales_trend[3:],
                            mode='lines+markers',
                            name='AI Forecast',
                            line=dict(color='#3B82F6', width=4, dash='dot'),
                            marker=dict(size=10, symbol='star')
                        ))
                        
                        # Deep, cinematic layout styling
                        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(10,10,10,0.5)',
                            font=dict(color='#E5E7EB'),
                            xaxis=dict(showgrid=False),
                            yaxis=dict(gridcolor='#374151', title="Units Sold / Demanded"),
                            margin=dict(l=0, r=0, t=30, b=0)
                        )
                        
                        # Render the chart in Streamlit
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("---")
                        # --------------------------------------

                        st.markdown("### Status Alert")
                        if data["inventory_status"] == "Stockout Risk High":
                            st.error("🚨 CRITICAL: Stockout Risk High. Immediate reorder recommended.")
                        else:
                            st.success("✅ Stock Optimal. No immediate action required.")
                    else:
                        st.error(f"API Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    # --- TAB 2: Bulk Upload Logic ---
    with tab2:
        st.header("Bulk Batch Processing")
        st.info("Upload a CSV file containing historical data for multiple SKUs to generate a batch forecast report.")
        
        uploaded_file = st.file_uploader("Upload Inventory CSV", type=["csv"])
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of Uploaded Data:")
            st.dataframe(df.head()) 
            
            if st.button("Run Batch AI Forecast"):
                results = []
                progress_bar = st.progress(0)
                
                with st.spinner("Processing bulk records through FastAPI..."):
                    for index, row in df.iterrows():
                        payload = row.to_dict()
                        try:
                            res = requests.post("https://sane-inventory-forecaster.onrender.com/predict", json=payload)
                            if res.status_code == 200:
                                results.append(res.json())
                        except Exception as e:
                            pass 
                        progress_bar.progress((index + 1) / len(df))
                
                if results:
                    st.success("Batch Processing Complete!")
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df)
                    
                    csv_export = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download AI Forecast Report (CSV)",
                        data=csv_export,
                        file_name='wfx_bulk_forecast_results.csv',
                        mime='text/csv',
                    )

# --- 6. Main Routing Logic ---
if not st.session_state.get("logged_in", False):
    login_page()
else:
    main_dashboard()