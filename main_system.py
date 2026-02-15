from database import MongoHandler
from vectorstore import KnowledgeBase
from asisstant import create_farmer_agent

# 1. Initialize DBs
import os

MONGO_URI = os.getenv("MONGO_URI")  # <- gets it from environment variable
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

mongo = MongoHandler(MONGO_URI)
#mongo = MongoHandler("mongodb+srv://farmer_admin:Roronoa123@newmain.t1vt5ne.mongodb.net/?appName=NewMain")
kb = KnowledgeBase()

# 2. Add some initial farming knowledge (One-time setup)
farming_knowledge = [
    "Maize needs irrigation every 10 days in dry seasons.",
    "Blight disease in Maize causes gray leaf spots; treat with fungicide.",
    "Harvest Maize when the husks turn brown and kernels are hard."
]
kb.create_knowledge_base(farming_knowledge)

# 3. Predict & Save (Logic from your previous steps)
# mongo.save_crop_analysis("Maize", {"market": "Dahod", "price": 442}, "Increasing", "SELL IMMEDIATELY")

# 4. Start Assistant
assistant = create_farmer_agent(mongo, kb)

# --- Test Query ---
query = "Should I sell my Maize today or wait? Also, how do I treat leaf spots?"
response = response = assistant.ask(query)


print("\n\nAI ASSISTANT RESPONSE:\n", response)