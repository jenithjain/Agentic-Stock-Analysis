"""
Agent for calculating stock price changes over time.
"""

import requests
import datetime
from src.config.config import ALPHA_VANTAGE_API_KEY, DEFAULT_TIMEFRAME_DAYS

class TickerPriceChangeAgent:
    def __init__(self):
        self.api_key = ALPHA_VANTAGE_API_KEY
        
    def get_price_change(self, ticker, days=None):
        """
        Calculate price change over a specified timeframe.
        
        Args:
            ticker (str): Stock ticker symbol
            days (int, optional): Number of days to look back. Defaults to DEFAULT_TIMEFRAME_DAYS.
            
        Returns:
            dict: Price change information
        """
        if days is None:
            days = DEFAULT_TIMEFRAME_DAYS
            
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={self.api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if "Time Series (Daily)" not in data:
                return None
                
            time_series = data["Time Series (Daily)"]
            dates = sorted(time_series.keys(), reverse=True)
            
            # Get today's or most recent price
            latest_date = dates[0]
            latest_price = float(time_series[latest_date]["4. close"])
            
            # Get price from n days ago or closest available
            target_date_index = min(days, len(dates) - 1)
            past_date = dates[target_date_index]
            past_price = float(time_series[past_date]["4. close"])
            
            # Calculate change
            absolute_change = latest_price - past_price
            percent_change = (absolute_change / past_price) * 100
            
            return {
                "symbol": ticker,
                "latest_date": latest_date,
                "latest_price": latest_price,
                "past_date": past_date,
                "past_price": past_price,
                "absolute_change": absolute_change,
                "percent_change": percent_change,
                "days": days
            }
        except Exception as e:
            print(f"Error calculating price change: {e}")
            return None