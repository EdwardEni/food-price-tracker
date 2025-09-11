import pandas as pd
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger("price_alerts")

class PriceAlert:
    def __init__(self, threshold_percent=20, lookback_days=30):
        self.threshold_percent = threshold_percent
        self.lookback_days = lookback_days
        
    def detect_spike(self, current_price, historical_prices):
        """Detect if current price is a spike compared to historical data"""
        if not historical_prices or len(historical_prices) < 7:
            return False
            
        avg_price = np.mean(historical_prices)
        price_change = ((current_price - avg_price) / avg_price) * 100
        
        if price_change > self.threshold_percent:
            logger.warning(f"Price spike detected: {price_change:.2f}% increase")
            return True, price_change
            
        return False, price_change

# Example usage in your forecast code
alert_system = PriceAlert(threshold_percent=25)

# After generating forecasts, check for spikes
def check_for_alerts(forecast_df):
    for index, row in forecast_df.iterrows():
        # Simulate historical prices (replace with actual data)
        historical_prices = [row['yhat'] * 0.8, row['yhat'] * 0.9, row['yhat'] * 0.85]
        
        is_spike, percent_change = alert_system.detect_spike(
            row['yhat'], historical_prices
        )
        
        if is_spike:
            send_alert(
                product_id=f"{row['admin_id']}_{row['mkt_id']}_{row['cm_id']}",
                current_price=row['yhat'],
                percent_change=percent_change,
                forecast_date=row['ds']
            )
