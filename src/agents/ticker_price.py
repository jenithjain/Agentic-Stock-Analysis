"""
Agent for retrieving current stock price.
"""

import requests
import time
from src.config.config import ALPHA_VANTAGE_API_KEY

class TickerPriceAgent:
    def __init__(self):
        self.api_key = ALPHA_VANTAGE_API_KEY
        
    def get_price(self, ticker):
        """
        Get current price for a stock ticker.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            dict: Price information including current price and change percentage
        """
        # Try Global Quote endpoint first
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={self.api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            # Check for API limit message
            if "Note" in data and "API call frequency" in data["Note"]:
                print("API rate limit reached. Waiting before retrying...")
                time.sleep(15)  # Wait 15 seconds before retrying
                response = requests.get(url)
                data = response.json()
            
            if "Global Quote" in data and data["Global Quote"] and "05. price" in data["Global Quote"]:
                return {
                    "price": data["Global Quote"]["05. price"],
                    "change_percent": data["Global Quote"]["10. change percent"].strip('%')
                }
            
            # If Global Quote fails, try TIME_SERIES_DAILY
            time.sleep(1)  # Small delay to avoid API rate limiting
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            # Check for API limit message
            if "Note" in data and "API call frequency" in data["Note"]:
                print("API rate limit reached. Waiting before retrying...")
                time.sleep(15)  # Wait 15 seconds before retrying
                response = requests.get(url)
                data = response.json()
            
            if "Time Series (Daily)" in data and data["Time Series (Daily)"]:
                # Get the latest date
                latest_date = list(data["Time Series (Daily)"].keys())[0]
                latest_data = data["Time Series (Daily)"][latest_date]
                
                # Get previous date for calculating change
                prev_date = list(data["Time Series (Daily)"].keys())[1]
                prev_data = data["Time Series (Daily)"][prev_date]
                
                # Calculate price change percentage
                current_price = float(latest_data["4. close"])
                prev_price = float(prev_data["4. close"])
                change_percent = ((current_price - prev_price) / prev_price) * 100
                
                return {
                    "price": str(current_price),
                    "change_percent": str(round(change_percent, 2))
                }
                
            # If all attempts fail, return None
            return None
            
        except Exception as e:
            print(f"Error fetching price data: {e}")
            return None