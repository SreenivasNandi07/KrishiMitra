'''import pandas as pd
import ollama
from Crop_prices_predict import PricePredictor 
from Best_mandi import get_best_mandi
from storage_advisor import storage_advisor

class FarmerAssistant:
    def __init__(self, mongo, kb):
        self.mongo = mongo
        self.kb = kb
        self.model = "llama3"
        self.price_engine = PricePredictor()
        self.df = pd.DataFrame()
        
        try:
            # Connect to the exact collection defined in database.py
            cursor = self.mongo.collection.find({})
            data_list = list(cursor)
            
            if data_list:
                self.df = pd.DataFrame(data_list)
                # WE DO NOT LOWERCASE COLUMNS HERE anymore.
                # This keeps "Commodity", "Market", etc., exactly as they are in the CSV.
                print(f"✅ Assistant connected! Loaded {len(self.df)} rows from MongoDB.")
            else:
                print("❌ MongoDB found, but 'crop_insights' is empty. Run upload_data.py!")
        except Exception as e:
            print(f"❌ Connection Error in Assistant: {e}")

    def ask(self, user_query):
        if self.df.empty:
            return "Namaste! I'm having trouble accessing my crop database. Please ensure the data is uploaded."

        try:
            # 1. Flexible Crop Detection
            # We match the query and format it to Title Case for your specialists
            detected_crop = "Wheat" # Default
            for crop in ["Wheat", "Rice", "Maize", "Cotton", "Gram"]:
                if crop.lower() in user_query.lower():
                    detected_crop = crop
                    break
            
            # 2. Specialist: Best Mandi
            # Since we didn't lowercase self.df, it will find "Commodity" perfectly.
            mandi_info = get_best_mandi(self.df, detected_crop)
            
            current_price = 0
            mandi_name = "Local Market"
            
            if isinstance(mandi_info, dict):
                current_price = mandi_info.get('price', 0)
                mandi_name = mandi_info.get('market', 'Local Market')

            # 3. Specialist: Price Prediction (Calling your LSTM engine)
            # Change this to whatever method name you used in Crop_prices_predict.py
            try:
                # Assuming you have a prediction method ready
                predicted_price = current_price * 1.05 
            except:
                predicted_price = current_price

            # 4. Specialist: Storage Advice
            advice = storage_advisor(current_price, predicted_price, "Increasing")

            # 5. The "Brain" (Llama 3)
            prompt = f"""
            SYSTEM: You are AgriMind-AI, a grounded, witty, and supportive AI peer for farmers. 
        Your goal is to be helpful and conversational. Don't sound like a dry textbook. 
        If the user says something simple like 'Hi', don't dump a whole data report; 
        just be friendly and ask how their fields are doing.
            User Query: {user_query}
            
            DATA REPORT:
            - Crop: {detected_crop}
            - Best Market: {mandi_name}
            - Current Price: ₹{current_price}
            - Predicted Price: ₹{predicted_price:.2f}
            - Storage Strategy: {advice}
            
            As an expert agricultural assistant, explain these findings to the farmer in a warm, helpful way.
            INSTRUCTIONS:
        1. Keep it friendly. If they ask about one crop but you have data for another, 
           clarify that first.
        2. Use the CONTEXT DATA only when they ask for analysis or if it's 
           the crop they are interested in.
        3. If you're giving advice, sound like a peer, not a lecturer.
            """
            
            response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
            return response['message']['content']

        except Exception as e:
            return f"Namaste! I hit a snag while talking to my specialists: {str(e)}"

def create_farmer_agent(mongo, kb):
    return FarmerAssistant(mongo, kb)'''


import pandas as pd
import ollama

from Crop_prices_predict import PricePredictor
from Best_mandi import get_best_mandi
from demand_predict import predict_demand_trend
from storage_advisor import storage_advisor

SUPPORTED_CROPS = {
    "wheat": "Wheat",
    "onion": "Onion",
    "potato": "Potato",
    "maize": "Maize",
    "groundnut": "Groundnut",
    "cotton": "Cotton"
}

class FarmerAssistant:
    def __init__(self, mongo, kb):
        self.mongo = mongo
        self.kb = kb
        self.model = "llama3"
        self.price_engine = PricePredictor()

        cursor = self.mongo.collection.find({})
        self.df = pd.DataFrame(list(cursor))

        if self.df.empty:
            print("❌ No crop data found in MongoDB")
        else:
            print(f"✅ Loaded {len(self.df)} crop records")

    def detect_crop(self, text: str):
        for key, value in SUPPORTED_CROPS.items():
            if key in text.lower():
                return value
        return None

    def ask(self, user_query: str):
        if self.df.empty:
            return "I cannot access crop data right now."

        crop = self.detect_crop(user_query)
        if not crop:
            return "Please mention a crop like wheat, onion, potato, maize, groundnut, or cotton."

        # 1️⃣ Best mandi
        mandi_data = get_best_mandi(self.df, crop)
        if not mandi_data:
            return f"No mandi data available for {crop}"

        current_price = mandi_data["price"]

        # 2️⃣ Demand prediction
        try:
            trend, demand_prices = predict_demand_trend(self.df, crop)
        except Exception as e:
            trend = "Stable"
            demand_prices = []

        # 3️⃣ Price prediction (LSTM)
        try:
            future_prices = self.price_engine.predict(self.df, crop)
            predicted_price = future_prices[-1]
        except Exception:
            predicted_price = current_price
            future_prices = []

        # 4️⃣ Storage advice
        advice = storage_advisor(current_price, predicted_price, trend)

        # 5️⃣ Save to Mongo (analysis result)
        self.mongo.save_crop_analysis(
            crop=crop,
            mandi_data=mandi_data,
            trend=trend,
            advice=advice
        )

        # 6️⃣ LLM explanation
        prompt = f"""
Farmer Query: {user_query}

Crop: {crop}
Best Market: {mandi_data['market']} ({mandi_data['district']}, {mandi_data['state']})
Current Price: ₹{current_price}
Demand Trend: {trend}
Predicted Price (7 days): ₹{predicted_price:.2f}
Storage Advice: {advice}

Explain clearly and practically.
"""

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

def create_farmer_agent(mongo, kb):
    return FarmerAssistant(mongo, kb)
