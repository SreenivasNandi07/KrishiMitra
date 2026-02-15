"""
import pandas as pd

def get_best_mandi(df, commodity_name):
    
    Identifies which market is currently paying the highest price for the crop.
    
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
    }"""
# works
"""
import pandas as pd

def get_best_mandi(df, crop):
    data = df[df["Commodity"] == crop].copy()
    if data.empty:
        return None

    data["Arrival_Date"] = pd.to_datetime(data["Arrival_Date"])
    latest = data[data["Arrival_Date"] == data["Arrival_Date"].max()]

    row = latest.loc[latest["Modal_Price"].idxmax()]
    return {
        "market": row["Market"],
        "district": row["District"],
        "state": row["State"],
        "price": float(row["Modal_Price"]),
        "date": row["Arrival_Date"].strftime("%Y-%m-%d")
    }
"""
import pandas as pd

def get_best_mandi(df, crop):
    
    df = df.copy()
    df.columns = df.columns.str.lower()

    data = df[df["commodity"] == crop]
    if data.empty:
        return None

    data["arrival_date"] = pd.to_datetime(data["arrival_date"])
    latest_date = data["arrival_date"].max()
    latest = data[data["arrival_date"] == latest_date]

    best = latest.loc[latest["modal_price"].idxmax()]

    return {
        "market": best["market"],
        "district": best.get("district", ""),
        "state": best.get("state", ""),
        "price": float(best["modal_price"]),
        "date": latest_date.strftime("%Y-%m-%d")
    }
