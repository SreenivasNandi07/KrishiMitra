'''
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
from asisstant import create_farmer_agent # Ensure filename is asisstant.py
from database import MongoHandler
from vectorstore import KnowledgeBase

# --- 1. INITIALIZATION ---
app = FastAPI(title="AgriMind AI API")

# Setup connections
MONGO_URI = "mongodb+srv://farmer_admin:Roronoa123@newmain.t1vt5ne.mongodb.net/?appName=NewMain/" 
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
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

# Import your custom modules
try:
    from asisstant import create_farmer_agent
    from database import MongoHandler
    from vectorstore import KnowledgeBase
except ImportError as e:
    print(f"CRITICAL ERROR: Could not find a module. {e}")

app = FastAPI(title="AgriMind AI API")

# Define global variables but don't initialize them yet
mongo = None
kb = None
assistant = None

class Query(BaseModel):
    query: str
    crop: str = "Wheat"

# --- LIFESPAN STARTUP ---
@app.on_event("startup")
async def startup_event():
    global mongo, kb, assistant
    print("Connecting to Database and loading AI... Please wait.")
    try:
        MONGO_URI = "mongodb+srv://farmer_admin:Roronoa123@newmain.t1vt5ne.mongodb.net/?appName=NewMain/" 
        mongo = MongoHandler(MONGO_URI)
        kb = KnowledgeBase()
        assistant = create_farmer_agent(mongo, kb)
        print("✅ AgriMind AI is ready!")
    except Exception as e:
        print(f"❌ FAILED TO START: {e}")

# --- ENDPOINTS ---

@app.post("/predict-price")
async def get_prediction(data: Query):
    return {"prediction": [900, 920, 915, 930, 945, 950, 960]}

@app.post("/best-mandi")
async def get_mandi(data: Query):
    # Check if assistant loaded properly
    if not assistant or not hasattr(assistant, 'df'):
        return {"mandi": {"mandi": "Error", "price": "N/A"}}
    
    # Simple logic to filter your dataframe
    df = assistant.df
    crop_data = df[df['item_name'].str.contains(data.crop, case=False)]
    if not crop_data.empty:
        best = crop_data.sort_values(by='price', ascending=False).iloc[0]
        return {"mandi": {"mandi": best['mandi_name'], "price": best['price']}}
    return {"mandi": {"mandi": "Not Found", "price": "N/A"}}

@app.post("/ask-ai")
async def ask_assistant(data: Query):
    if not assistant:
        return {"answer": "AI is still loading or failed to start."}
    response = await asyncio.to_thread(assistant.ask, data.query)
    return {"answer": response}

if __name__ == "__main__":
    # Try running on port 8001 if 8000 is giving "CancelledError"
    uvicorn.run(app, host="127.0.0.1", port=8000)