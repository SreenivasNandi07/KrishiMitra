def recommend_best_mandi(df, commodity_name, state=None):
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
    }