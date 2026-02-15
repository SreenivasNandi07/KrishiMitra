# AgriMind AI - Requirements

## 1. Overview
AgriMind AI is a smart farming assistant that provides farmers with insights on crop prices, storage recommendations, demand trends, and the best market (“mandi”) for selling their crops. The system leverages:

- AI language models (Ollama LLM) for natural language query responses.
- Machine learning (LSTM) for price prediction.
- MongoDB Atlas for data storage.
- FastAPI for backend APIs.
- Streamlit for the frontend dashboard.

---

## 2. Functional Requirements

### 2.1 User Queries
- Users can ask natural language questions about crops.
- The assistant detects the crop, analyzes demand, predicts prices, and provides storage advice.
- Supports multiple languages (English, Hindi, Telugu).

### 2.2 Crop Price Prediction
- Predicts next 7-day crop prices using an LSTM model.
- Inputs historical prices from MongoDB.
- Provides forecast trend and percentage changes.

### 2.3 Best Mandi Recommendation
- Finds the market with the highest current price for a given crop.
- Uses historical crop arrival and price data from MongoDB.

### 2.4 Demand Trend Analysis
- Provides demand trend for a crop using AI predictions.
- Trend categorized as Increasing, Decreasing, or Stable.

### 2.5 Storage Recommendations
- Advises whether to store or sell based on current price, predicted price, and demand trend.

### 2.6 Data Upload & Management
- Upload crop data CSV to MongoDB.
- Create vector embeddings for AI assistant knowledge base using FAISS.

---

## 3. Non-Functional Requirements

### 3.1 Performance
- API response time for AI queries should be <5 seconds.
- Price prediction LSTM should complete within 2 minutes for 1000+ records.

### 3.2 Scalability
- MongoDB Atlas allows handling large crop datasets.
- FAISS vector store scales with knowledge base growth.

### 3.3 Reliability
- MongoDB provides persistence for crop insights.
- API services run inside Docker for isolated and reproducible environments.

### 3.4 Security
- MongoDB Atlas secured with username/password.
- Sensitive URIs (MongoDB URI) injected as environment variables.
- HTTPS can be configured for Streamlit and FastAPI deployment.

---

## 4. Technical Requirements

### 4.1 Backend
- Python 3.11
- FastAPI
- Uvicorn
- asyncio
- pymongo
- pandas
- NumPy
- torch (PyTorch)
- scikit-learn

### 4.2 Frontend
- Streamlit
- requests (for API communication)

### 4.3 AI / ML
- Ollama LLM for query response
- PyTorch for LSTM price prediction
- FAISS & HuggingFace embeddings for vector search knowledge base

### 4.4 Infrastructure
- Docker (containerized environment)
- MongoDB Atlas (cloud database)
- Optional: VS Code / Kiros for development

---

## 5. Data Requirements
- Crop historical prices CSV (columns: Commodity, Market, State, Modal_Price, Arrival_Date)
- Knowledge base texts for farming manuals
- MongoDB collection structure:
  - `crop_insights` collection
    - crop
    - last_updated
    - best_mandi
    - demand_trend
    - storage_advice
