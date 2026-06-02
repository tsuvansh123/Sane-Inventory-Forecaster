# 📦 SANE Inventory Forecaster

# Overview
  The *SANE Inventory Forecaster* is a full-stack predictive analytics dashboard designed specifically for apparel supply chain optimization. This tool leverages machine learning to predict 30-day inventory demand, helping warehouse managers minimize stockout risks and maintain optimal inventory levels.

# Live demo - https://sane-inventory-forecaster-dlwabvruvol5bardxhdfaz.streamlit.app/

# System Architecture
  This project is built using a modern, decoupled client-server architecture:
* Frontend (UI):Built with *Streamlit* and deployed on Streamlit Community Cloud. It provides an interactive dashboard for users to input real-time warehouse metrics (SKU, current stock, vendor lead times).
* Backend (API): A RESTful API built with **FastAPI** and **Uvicorn**, deployed on **Render**. It securely hosts the machine learning engine and processes incoming prediction requests.
* Machine Learning Engine: Powered by an **XGBoost** regression model trained on historical retail data to identify seasonal trends and demand spikes.

# Tech Stack
* Language: Python 3.11+
* Machine Learning: XGBoost, Pandas, Scikit-learn, Joblib
* Backend: FastAPI, Pydantic, Uvicorn, Requests
* Frontend: Streamlit
* Deployment: Render (Backend API), Streamlit Community Cloud (Frontend UI), Git/GitHub

# Key Features
* Instant AI Forecasting: Calculates predicted 30-day demand instantly via API POST requests.
* Dynamic Reorder Logic: Automatically factors in vendor lead times and current stock to suggest exact reorder quantities.
* Status Alerts: Provides visual indicators (Stock Optimal vs. Stockout Risk High) to drive immediate logistical action.
