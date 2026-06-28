📦 SANE Inventory Forecaster
Overview
The SANE Inventory Forecaster is a full-stack predictive analytics platform combining machine learning and large language model intelligence, designed specifically for apparel supply chain optimization. The platform forecasts 30-day inventory demand using XGBoost and lets non-technical stakeholders — buyers, merchandisers, supply chain managers — query those predictions in plain English via a Gemini 2.0 Flash powered chat interface.
Live Demo → https://sane-inventory-forecaster-dlwabvruvol5bardxhdfaz.streamlit.app/

System Architecture
Built on a modern, decoupled client-server architecture with three distinct layers:

Frontend (UI): Built with Streamlit and deployed on Streamlit Community Cloud. Three-tab interface — Tab 1 & 2 for forecast input and results, Tab 3 (Ask AI Analyst) for natural language querying of forecast outputs via a conversational chat UI.
Backend (API): A RESTful API built with FastAPI and Uvicorn, deployed on Render. Hosts two core endpoints — /predict for XGBoost inference and /query for Gemini LLM routing. Handles all ML computation and LLM communication server-side.
Machine Learning Engine: XGBoost regression model trained on historical retail data to identify seasonal trends and non-linear demand spikes across SKUs.
LLM Layer (Gemini 2.0 Flash): Integrated via the official Google GenAI SDK. The /query endpoint builds a structured prompt by injecting the live XGBoost forecast table and passes it to Gemini 2.0 Flash, returning plain-English answers in 2–3 seconds. No LangChain, no RAG — direct prompt engineering chosen deliberately for structured, session-scoped data.


Tech Stack
LayerTechnologyLanguagePython 3.11+Machine LearningXGBoost, Scikit-learn, Pandas, JoblibLLMGemini 2.0 Flash, Google GenAI SDKBackendFastAPI, Pydantic, Uvicorn, RequestsFrontendStreamlitDeploymentRender (Backend), Streamlit Community Cloud (Frontend)Version ControlGit, GitHub

Key Features

30-Day Demand Forecasting: XGBoost model delivers SKU-level inventory demand predictions instantly via API POST requests.
Natural Language Q&A (Ask AI Analyst): Users type questions like "Which SKUs are at highest stockout risk?" or "Summarise key findings in 3 bullet points" — Gemini reads the live forecast output and responds in plain English within seconds.
Dynamic Reorder Logic: Automatically factors in vendor lead times and current stock levels to suggest precise reorder quantities per SKU.
Status Alerts: Visual indicators (Stock Optimal / Stockout Risk High) for immediate operational action.
Secure Access & Custom Data: Authentication layer and dynamic CSV ingestion so teams can run forecasts on their own datasets.


Why No LangChain?
A deliberate architectural choice. The forecast data is small, structured, and changes every session — making vector databases and retrieval pipelines unnecessary overhead. Direct prompt engineering with the full XGBoost output table passed in context is faster, simpler, and more accurate for this use case.
