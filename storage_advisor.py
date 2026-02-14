'''def storage_advisor(current_price, predicted_7day_price, demand_trend):
    """
    Logic: If predicted price > current price + storage cost (approx 2-5%), then store.
    """
    price_diff_pct = ((predicted_7day_price - current_price) / current_price) * 100
    storage_cost_pct = 2.0  # Assumed weekly storage/opportunity cost
    
    if price_diff_pct > storage_cost_pct:
        advice = "STORE: Prices are expected to rise significantly."
    elif price_diff_pct > 0:
        advice = "SELL: Prices are stable, but storage costs might outweigh gains."
    else:
        advice = "SELL IMMEDIATELY: Price trend is downward."
        
    if demand_trend == "Increasing":
        advice += " (High market demand expected soon)."
        
    return advice'''

def storage_advisor(current_price, predicted_7day_price, demand_trend):
    """
    Returns advice on whether to store or sell based on price gap and demand.
    """
    # Calculate percentage change
    price_diff_pct = ((predicted_7day_price - current_price) / current_price) * 100
    storage_cost_pct = 2.0  # Assumed cost of storage/wastage per week
    
    if price_diff_pct > (storage_cost_pct + 3): # If gain is > 5%
        advice = "STRATEGY: STORE. Predicted price rise covers storage costs."
    elif price_diff_pct > 0:
        advice = "STRATEGY: SELL. Marginal gain, but not worth the storage risk."
    else:
        advice = "STRATEGY: SELL IMMEDIATELY. Prices are trending downward."
        
    if demand_trend == "Increasing":
        advice += " Market demand is rising, which supports holding stock."
        
    return advice