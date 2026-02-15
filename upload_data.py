"""import pandas as pd
from pymongo import MongoClient
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

#This code will upload datasets to mongodb


# 1. Setup Connections
MONGO_URI = "mongodb+srv://farmer_admin:Roronoa123@newmain.t1vt5ne.mongodb.net/?appName=NewMain/" # Replace with your actual string
client = MongoClient(MONGO_URI)
db = client['farmer_assistant']
collection = db['crop_insights']

# 2. Load your CSV
csv_file = "data/2001.csv"
if not os.path.exists(csv_file):
    print(f"Error: {csv_file} not found! Make sure it's in the same folder.")
    exit()

df = pd.read_csv(csv_file)

# 3. Upload to MongoDB (The Silo)
print("Uploading data to MongoDB...")
collection.delete_many({}) # Clear old data if any
data_dict = df.to_dict("records")
collection.insert_many(data_dict)
print(f"Successfully uploaded {len(data_dict)} rows to MongoDB!")


# 4. Create FAISS Index (The Knowledge Base)
print("Creating local FAISS index...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Force all column names to lowercase to avoid errors
df.columns = df.columns.str.lower()

# Check for the correct column names
# We'll use whatever columns exist: state/district/market/commodity
knowledge_texts = []
for _, row in df.iterrows():
    # Use .get() to avoid crashing if a column is missing
    state = row.get('state', row.get('state_name', 'Unknown State'))
    commodity = row.get('commodity', row.get('crop', 'Unknown Crop'))
    market = row.get('market', 'Local Market')
    
    text = f"Information for {commodity} in {market}, {state}"
    knowledge_texts.append(text)

# Create and save the index
vector_db = FAISS.from_texts(knowledge_texts, embeddings)
vector_db.save_local("faiss_index")
print("FAISS index created successfully!")"""

import pandas as pd
from pymongo import MongoClient
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

MONGO_URI = "mongodb+srv://farmer_admin:Roronoa123@newmain.t1vt5ne.mongodb.net/?appName=NewMain/"
client = MongoClient(MONGO_URI)

db = client["farmer_assistant"]
collection = db["crop_insights"]

csv_file = "data/2001.csv"
if not os.path.exists(csv_file):
    raise FileNotFoundError("CSV file not found")

df = pd.read_csv(csv_file)

print("Uploading data to MongoDB...")
collection.delete_many({})
collection.insert_many(df.to_dict("records"))
print(f"Uploaded {len(df)} rows")

print("Creating FAISS index...")
df.columns = df.columns.str.lower()

texts = []
for _, row in df.iterrows():
    texts.append(
        f"{row.get('commodity','crop')} market price in {row.get('market','market')} {row.get('state','state')}"
    )

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.from_texts(texts, embeddings)
vector_db.save_local("faiss_index")

print("FAISS index created")
