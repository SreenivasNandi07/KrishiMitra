'''
# 1. First, make sure you have permission to run the script (Run this once)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 2. Now activate the environment
.\venv\Scripts\Activate.ps1 '''
# worked version
'''
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class FarmerAssistant:
    def __init__(self, mongo_handler, knowledge_base):
        self.llm = OllamaLLM(model="llama3.1")
        self.mongo = mongo_handler
        self.kb = knowledge_base
        self.parser = StrOutputParser()

    def ask(self, question):
        # 1. Fetch data from our tools manually
        # This replaces the "Agent" part that keeps breaking
        market_data = self.mongo.fetch_crop_insight("Maize")
        farming_advice = self.kb.search(question)

        # 2. Build a clear prompt with that data
        template = """
        You are a helpful Indian Agriculture Expert. 
        Use the following information to answer the farmer's question.

        MARKET DATA: {market}
        FARMING GUIDES: {guides}

        QUESTION: {question}

        ANSWER:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # 3. Create the Chain
        chain = prompt | self.llm | self.parser
        
        # 4. Run it
        return chain.invoke({
            "market": str(market_data),
            "guides": farming_advice,
            "question": question
        })

# Function for FastAPI to call
def create_farmer_agent(mongo_handler, knowledge_base):
    return FarmerAssistant(mongo_handler, knowledge_base)
    '''
import ollama
from database import MongoHandler
'''from Crop_prices_predict import predict_price  # Your specialist 1
from storage_advisor import get_storage_tips    # Your specialist 2
from Best_mandi import suggest_best_mandi       # Your specialist 3

class FarmerAssistant:
    def __init__(self):
        # Initialize your MongoDB handler
        self.db = MongoHandler()
        self.model = "llama3"

    def ask(self, user_query):
        """
        The main engine: Detects crop, runs specialists, and generates response.
        """
        # 1. SIMPLE CROP DETECTION
        # You can make this more advanced, but for now, we check the text
        crops = ["wheat", "rice", "maize", "cotton", "gram"]
        detected_crop = None
        for crop in crops:
            if crop in user_query.lower():
                detected_crop = crop
                break

        # 2. RUN SPECIALISTS (If a crop is found)
        specialist_data = ""
        if detected_crop:
            print(f"--- Specialist System Activated for: {detected_crop} ---")
            
            # Get Price Prediction (from your ML model file)
            p_price = predict_price(detected_crop)
            
            # Get Storage Advice (from your storage advisor file)
            s_tips = get_storage_tips(detected_crop)
            
            # Get Market Advice (from your Best Mandi file)
            mandi = suggest_best_mandi(detected_crop)
            
            # Combine this data into a 'Context' for the AI
            specialist_data = f"""
            REAL-TIME DATA FOR {detected_crop.upper()}:
            - Predicted Market Price: {p_price}
            - Storage Requirement: {s_tips}
            - Recommended Market: {mandi}
            """

        # 3. CONSTRUCT THE PROMPT
        system_prompt = f"""
        You are a helpful Indian Agriculture Assistant. 
        Use the following specialist data to answer the farmer's question.
        If no specialist data is provided, give general farming advice.
        
        {specialist_data}
        
        Answer in a friendly, professional manner. Use 'Namaste' and keep it simple.
        """

        # 4. GET RESPONSE FROM LLAMA 3
        response = ollama.chat(model=self.model, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_query},
        ])

        return response['message']['content']

# Example usage for testing
if __name__ == "__main__":
    assistant = FarmerAssistant()
    print(assistant.ask("What is the situation with wheat in Rajkot?"))'''

    # Import your actual specialist files
import pandas as pd
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
            User Query: {user_query}
            
            DATA REPORT:
            - Crop: {detected_crop}
            - Best Market: {mandi_name}
            - Current Price: ₹{current_price}
            - Predicted Price: ₹{predicted_price:.2f}
            - Storage Strategy: {advice}
            
            As an expert agricultural assistant, explain these findings to the farmer in a warm, helpful way.
            """
            
            response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
            return response['message']['content']

        except Exception as e:
            return f"Namaste! I hit a snag while talking to my specialists: {str(e)}"

def create_farmer_agent(mongo, kb):
    return FarmerAssistant(mongo, kb)