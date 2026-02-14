'''import pandas as pd
import torch
from Crop_prices_predict import PricePredictor # Assuming your code is in price_predictor.py

# 1. Load the dataset
df = pd.read_csv('data/2001.csv')

# 2. Initialize the Predictor
predictor = PricePredictor()

# 3. Select a specific crop (e.g., 'Maize')
# This filters the data specifically for one model
crop_name = 'Maize' 
print(f"--- Preparing data for {crop_name} ---")

try:
    # 4. Preprocess and Scale the data
    scaled_data = predictor.prepare_data(df, crop_name)

    # 5. Create Sequences (60 days input -> 7 days output)
    X, y = predictor.create_sequences(scaled_data)

    # 6. Run Training
    print("Starting Training...")
    predictor.train_model(X, y, epochs=100)

    # 7. Make a Prediction for the NEXT 7 days
    # We take the most recent 60 days from our data to predict the future
    last_60_days = torch.tensor(scaled_data[-60:], dtype=torch.float32).unsqueeze(0)
    
    predictor.model.eval()
    with torch.no_grad():
        future_prediction = predictor.model(last_60_days)
        
    # 8. Inverse Transform to get actual prices back from 0-1 scale
    # (Note: This requires a bit of reshaping based on your scaler)
    print("Predicted Prices for next 7 days:", future_prediction.numpy())

except Exception as e:
    print(f"Error: {e}. Ensure you have at least 67 days of data for this crop.")'''

import pandas as pd
import torch
import numpy as np

# Import your modules
from Crop_prices_predict import PricePredictor # The LSTM class we built earlier
from demand_predict import predict_demand_trend
from storage_advisor import storage_advisor
from Best_mandi import get_best_mandi

# 1. Load Data
df = pd.read_csv('data/2001.csv')
CROP = '' # Change this to 'Onion', 'Potato', 'Sunflower', 'Black gram',etc.

print(f"--- Analysis for {CROP} ---")

# 2. Get Best Mandi Recommender
best_mandi = get_best_mandi(df, CROP)
print(f"Top Market Recommendation: {best_mandi['market']} at ₹{best_mandi['price']}")

# 3. Predict Demand Trend
trend, future_demand_prices = predict_demand_trend(df, CROP)
print(f"7-Day Demand Trend: {trend}")

# 4. Predict Prices using LSTM
predictor = PricePredictor()
scaled_data = predictor.prepare_data(df, CROP)
X_seq, y_seq = predictor.create_sequences(scaled_data)

# Simple Training (In production, load a pre-trained .pth model)
predictor.train_model(X_seq, y_seq, epochs=20)

# Get the last 60 days to predict next 7
last_window = torch.tensor(scaled_data[-60:], dtype=torch.float32).unsqueeze(0)
with torch.no_grad():
    prediction_scaled = predictor.model(last_window).numpy()[0]

# Denormalize (Approximate back to price)
current_price = best_mandi['price']
# Simple scaling back (prediction_scaled is 0 to 1)
avg_predicted_price = current_price * (1 + (prediction_scaled.mean() - 0.5) * 0.1)

# 5. Get Storage Advice
advice = storage_advisor(current_price, avg_predicted_price, trend)
print(f"Storage Advice: {advice}")

# 6. Save to MongoDB (Optional)
# save_to_mongodb(CROP, avg_predicted_price, trend, best_mandi)