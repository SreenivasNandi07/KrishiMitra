

<<<<<<< HEAD
=======
# Setup connections
MONGO_URI = "" 
mongo = MongoHandler(MONGO_URI)
kb = KnowledgeBase()
assistant = create_farmer_agent(mongo, kb)

# --- 2. MODELS ---
class Query(BaseModel):
    query: str
    crop: str = "Wheat"

# --- 3. HELPER FUNCTIONS ---
def get_best_mandi_logic(df, crop_name):
    """
    This is where your Mandi logic lives. 
    It filters your dataframe for the best price.
    """
    try:
        # Example logic: filter by crop and sort by price
        # Replace this with your actual dataframe filtering logic
        crop_data = df[df['item_name'].str.contains(crop_name, case=False)]
        best_row = crop_data.sort_values(by='price', ascending=False).iloc[0]
        return {
            "mandi": best_row['mandi_name'],
            "price": best_row['price'],
            "state": best_row['state']
        }
    except Exception:
        return {"mandi": "Market Not Found", "price": "N/A", "state": "N/A"}

# --- 4. ENDPOINTS ---

@app.get("/")
def home():
    return {"status": "Farmer API is Live", "docs": "/docs"}

@app.post("/predict-price")
async def get_prediction(data: Query):
    # Asynchronous mock for LSTM prediction
    await asyncio.sleep(0.1) 
    return {"prediction": [900, 920, 915, 930, 945, 950, 960]}

@app.post("/best-mandi")
async def get_mandi(data: Query):
    # This uses the helper function we defined above
    # We use assistant.df (assuming your assistant class stores the dataframe)
    mandi_data = get_best_mandi_logic(assistant.df, data.crop)
    return {"mandi": mandi_data}

@app.post("/ask-ai")
async def ask_assistant(data: Query):
    # This is the 'Slow' LLM task moved to a thread to keep the API responsive
    response = await asyncio.to_thread(assistant.ask, data.query)
    return {"answer": response}

# --- 5. EXECUTION ---
if __name__ == "__main__":
    import uvicorn
    # Use reload=True during development so it restarts when you save
    uvicorn.run("fastapi_worker:app", host="0.0.0.0", port=8000, reload=True)'''
>>>>>>> 5805811873bccb30d003b99b530f8a861d1869d3
import uvicorn
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

from database import MongoHandler
from vectorstore import KnowledgeBase
from asisstant import create_farmer_agent
from Best_mandi import get_best_mandi

app = FastAPI(title="AgriMind AI API")

mongo = None
kb = None
assistant = None

class Query(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    global mongo, kb, assistant
    mongo = MongoHandler(
        "mongodb+srv://farmer_admin:Roronoa123@newmain.t1vt5ne.mongodb.net/?appName=NewMain/"
    )
    kb = KnowledgeBase()
    assistant = create_farmer_agent(mongo, kb)
    print("AgriMind API ready")

@app.post("/ask-ai")
async def ask_ai(data: Query):
    return {
        "answer": await asyncio.to_thread(
            assistant.ask,
            data.query
        )
    }

@app.post("/best-mandi")
async def best_mandi(data: Query):
    crop = assistant.detect_crop(data.query)
    if not crop:
        return {"error": "Crop not detected"}

    return get_best_mandi(assistant.df, crop)

@app.post("/health")
async def health():
    return {"status": "ok"}
#new one added
@app.post("/predict-price")
async def predict_price(data: Query):
    crop = assistant.detect_crop(data.query)
    if not crop:
        return {"error": "Crop not detected"}

    try:
        future_prices = await asyncio.to_thread(
            assistant.price_engine.predict,
            assistant.df,
            crop
        )
        return {
            "crop": crop,
            "predicted_prices_next_7_days": future_prices
        }
    except Exception as e:
        return {
            "error": "Price prediction failed",
            "details": str(e)
        }


if __name__ == "__main__":
<<<<<<< HEAD
=======
    # Try running on port 8001 if 8000 is giving "CancelledError"
>>>>>>> 5805811873bccb30d003b99b530f8a861d1869d3
    uvicorn.run(app, host="127.0.0.1", port=8000)
