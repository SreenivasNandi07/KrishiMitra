# KrishiMitra - Design

## 1. System Architecture




- **Frontend (Streamlit UI):** Dashboard with tabs for AI queries, price predictor, best mandi, demand trend, and storage advisor.
- **Backend (FastAPI):** Receives requests, handles crop detection, ML predictions, and query routing.
- **Database (MongoDB Atlas):** Stores historical crop prices, insights, and predictions.
- **Vector Knowledge Base (FAISS):** Embeddings for farming manuals and best practices.
- **LLM (Ollama):** Generates natural language responses for user queries.

---

## 2. Component Design

### 2.1 FastAPI Worker
- Initializes MongoDB and Knowledge Base on startup.
- Provides API endpoints:
  - `/ask-ai` → returns AI response
  - `/predict-price` → returns 7-day forecast
  - `/best-mandi` → returns best market
  - `/health` → checks server status

### 2.2 AI Assistant (FarmerAssistant)
- Detects crop from query
- Retrieves best mandi data
- Predicts demand trend
- Runs LSTM-based price prediction
- Provides storage recommendations
- Returns response via Ollama LLM

### 2.3 LSTM Price Prediction
- Input: Past crop prices (resampled daily)
- Architecture: 2-layer LSTM with 64 hidden units, output 7 days
- Output: Normalized future prices rescaled to original price range

### 2.4 Knowledge Base
- Stores crop manuals as vectors
- Uses FAISS + HuggingFace embeddings
- Supports similarity search for queries

### 2.5 Data Upload
- CSV → MongoDB → FAISS embeddings
- Ensures vector DB is ready for AI queries

---

## 3. Docker & Environment Design

- **Dockerfile**:
  - Base: `python:3.11-slim`
  - Install dependencies from `requirements.txt`
  - Copy app code into container
  - CMD: `uvicorn fastapi_worker:app --host 0.0.0.0 --port 8000`
- **Environment Variables**:
  - `MONGO_URI` for MongoDB Atlas credentials
- **Ports**:
  - 8000 → FastAPI
  - 8501 → Streamlit (optional, can run separately)

---

## 4. Data Flow

1. Farmer enters query on Streamlit UI.
2. Frontend sends POST request to FastAPI endpoint.
3. FastAPI worker:
   - Detects crop
   - Fetches data from MongoDB
   - Predicts prices & demand
   - Calls Ollama LLM with context
4. Response returned to Streamlit and displayed to the user.

---

## 5. Notes for Hackathon Submission

- Highlight modularity: Backend, Frontend, AI modules separated.
- Mention Docker containerization for reproducibility.
- Include security note: MongoDB credentials stored in environment variables.
- Include diagram (ASCII or image) in design.md.
