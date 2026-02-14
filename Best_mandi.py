'''def recommend_best_mandi(df, commodity_name, state=None):
    """
    Finds the market with the highest current Modal_Price for a specific crop.
    """
    latest_date = df['Arrival_Date'].max()
    current_data = df[(df['Commodity'] == commodity_name) & (df['Arrival_Date'] == latest_date)]
    
    if state:
        current_data = current_data[current_data['State'] == state]
        
    if current_data.empty:
        return "No data available for today."
    
    # Sort by price descending
    best_mandi = current_data.sort_values(by='Modal_Price', ascending=False).iloc[0]
    
    return {
        "Market": best_mandi['Market'],
        "District": best_mandi['District'],
        "Price": best_mandi['Modal_Price'],
        "Recommendation": f"Sell at {best_mandi['Market']} for better margins."
    }'''
import pandas as pd

def get_best_mandi(df, commodity_name):
    """
    Identifies which market is currently paying the highest price for the crop.
    """
    crop_df = df[df['Commodity'] == commodity_name].copy()
    crop_df['Arrival_Date'] = pd.to_datetime(crop_df['Arrival_Date'])
    
    # Get the latest available records
    latest_date = crop_df['Arrival_Date'].max()
    latest_data = crop_df[crop_df['Arrival_Date'] == latest_date]
    
    if latest_data.empty:
        return None
    
    # Find the row with max Modal_Price
    best_row = latest_data.loc[latest_data['Modal_Price'].idxmax()]
    
    return {
        "market": best_row['Market'],
        "district": best_row['District'],
        "state": best_row['State'],
        "price": best_row['Modal_Price'],
        "date": latest_date.strftime('%Y-%m-%d')
    }