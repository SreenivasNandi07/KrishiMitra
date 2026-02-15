
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
    language: str = "English"

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
    if not data.query.strip():
        return {"error": "Query cannot be empty"}

    # Pass the language to the assistant
    return {
    "answer": await asyncio.to_thread(
        assistant.ask,
        data.query,
        data.language  # pass it here
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
    uvicorn.run(app, host="127.0.0.1", port=8000)



'''
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1 
uvicorn fastapi_worker:app --reload
http://127.0.0.1:8000/docs'''
