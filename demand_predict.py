from sklearn.ensemble import RandomForestRegressor

'''def predict_demand_trend(df, commodity_name):
    """
    Predicts if the arrival volume (demand/supply proxy) will increase or decrease.
    Note: If 'Arrivals' column is missing, we use Modal_Price volatility as a proxy.
    """
    crop_df = df[df['Commodity'] == commodity_name].copy()
    crop_df['Arrival_Date'] = pd.to_datetime(crop_df['Arrival_Date'])
    
    # Feature Engineering for Demand
    crop_df['Day'] = crop_df['Arrival_Date'].dt.day
    crop_df['Month'] = crop_df['Arrival_Date'].dt.month
    crop_df['DayOfWeek'] = crop_df['Arrival_Date'].dt.dayofweek
    
    # Target: Modal_Price as a proxy for market pressure if Arrivals volume is missing
    X = crop_df[['Day', 'Month', 'DayOfWeek']]
    y = crop_df['Modal_Price'] 
    
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    
    # Predict for next 7 days
    future_dates = pd.date_range(start=crop_df['Arrival_Date'].max(), periods=7)
    future_X = pd.DataFrame({
        'Day': future_dates.day,
        'Month': future_dates.month,
        'DayOfWeek': future_dates.dayofweek
    })
    
    preds = model.predict(future_X)
    trend = "Increasing" if preds[-1] > preds[0] else "Decreasing"
    return trend, preds'''
import pandas as pd


def predict_demand_trend(df, commodity_name):
    """
    Predicts if the market pressure (proxy for demand) will increase or decrease.
    """
    # Filter and Aggregate to get one price point per day
    #crop_df = df[df['Commodity'] == commodity_name].copy()
    crop_df = df[df['commodity'] == commodity_name.lower()].copy()

    #crop_df['Arrival_Date'] = pd.to_datetime(crop_df['Arrival_Date'])
    crop_df['arrival_date'] = pd.to_datetime(crop_df['arrival_date'])

    # We group by date to get a single trend line for the whole region
    daily_df = crop_df.groupby('Arrival_Date')['Modal_Price'].mean().reset_index()
    
    # Feature Engineering
    daily_df['Day'] = daily_df['Arrival_Date'].dt.day
    daily_df['Month'] = daily_df['Arrival_Date'].dt.month
    daily_df['DayOfWeek'] = daily_df['Arrival_Date'].dt.dayofweek
    
    X = daily_df[['Day', 'Month', 'DayOfWeek']]
    y = daily_df['Modal_Price'] 
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Predict for next 7 days
    last_date = daily_df['Arrival_Date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
    future_X = pd.DataFrame({
        'Day': future_dates.day,
        'Month': future_dates.month,
        'DayOfWeek': future_dates.dayofweek
    })
    
    preds = model.predict(future_X)
    # Trend based on the slope of the 7-day prediction
    trend = "Increasing" if preds[-1] > preds[0] else "Decreasing"
    return trend, preds