# 📦 SANE Inventory Forecaster

## Overview
The SANE Inventory Forecaster is a full-stack predictive analytics platform combining
machine learning and LLM intelligence, designed for apparel supply chain optimization.
Forecasts 30-day inventory demand using XGBoost and lets non-technical stakeholders
query predictions in plain English via a Groq-powered conversational interface.

**Live Demo** → https://sane-inventory-forecaster-dlwabvruvol5bardxhdfaz.streamlit.app/
Credentials for login page
username- admin
password- admin123

---

## System Architecture

- **Frontend (UI):** Streamlit — three-tab interface. Tab 1 & 2 for forecast input
  and results, Tab 3 (Ask AI Analyst) for natural language querying via chat UI.

- **Backend (API):** FastAPI + Uvicorn on Render. Two endpoints — /predict for
  XGBoost inference and /query for Groq LLM routing.

- **ML Engine:** XGBoost regression model trained on historical retail data to
  identify seasonal trends and non-linear demand spikes across SKUs.

- **LLM Layer (Groq API + LLaMA 3):** The /query endpoint builds a structured
  prompt injecting the live XGBoost forecast table and passes it to LLaMA 3 via
  Groq's inference API, returning plain-English answers in under 2 seconds.
  Groq chosen over closed models (Gemini, GPT-4) for free-tier availability
  and ultra-low latency. No LangChain, no RAG — direct prompt engineering.

---

## Tech Stack

| Layer        | Technology                              |
|--------------|-----------------------------------------|
| Language     | Python 3.11+                            |
| ML           | XGBoost, Scikit-learn, Pandas, Joblib   |
| LLM          | Groq API, LLaMA 3                       |
| Backend      | FastAPI, Pydantic, Uvicorn, Requests    |
| Frontend     | Streamlit                               |
| Deployment   | Render (Backend), Streamlit Cloud (Frontend) |
| Version Control | Git, GitHub                          |

---

## Key Features

- **30-Day Demand Forecasting:** XGBoost delivers SKU-level predictions via API.
- **Natural Language Q&A (Ask AI Analyst):** Ask "Which SKUs are at stockout risk?"
  — LLaMA 3 via Groq reads live forecast output and responds in under 2 seconds.
- **Dynamic Reorder Logic:** Factors in vendor lead times and current stock levels
  to suggest precise reorder quantities per SKU.
- **Status Alerts:** Visual indicators (Stock Optimal / Stockout Risk High).
- **Secure Access & Custom Data:** Auth layer + dynamic CSV ingestion.

---

## Why Groq over Gemini/GPT-4?
Groq offers free-tier inference at ultra-low latency using open-weight models like
LLaMA 3 — making it the right choice for a deployed student project with real users
and no billing overhead. For enterprise deployments requiring data privacy,
self-hosted models via Ollama would be the equivalent alternative.

## Why No LangChain?
Forecast data is small, structured, and session-scoped. Direct prompt engineering
with the full XGBoost output table passed in context is faster, simpler, and more
accurate than a retrieval pipeline for this use case.
