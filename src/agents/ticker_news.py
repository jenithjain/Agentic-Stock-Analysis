"""
Agent for retrieving news about a stock.
"""

import requests
import datetime
from src.config.config import ALPHA_VANTAGE_API_KEY

class TickerNewsAgent:
    def __init__(self):
        self.api_key = ALPHA_VANTAGE_API_KEY
        
    def get_news(self, ticker, limit=5):
        """
        Get recent news for a stock ticker.
        
        Args:
            ticker (str): Stock ticker symbol
            limit (int): Maximum number of news items to return
            
        Returns:
            list: List of news items with title, url, and date
        """
        # Extract base ticker without exchange suffix for better news results
        base_ticker = ticker.split('.')[0] if '.' in ticker else ticker
        
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={base_ticker}&apikey={self.api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if "feed" not in data or not data["feed"]:
                # Try with a more general search if specific ticker news not found
                url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&keywords={base_ticker}&apikey={self.api_key}"
                response = requests.get(url)
                data = response.json()
            
            if "feed" not in data:
                return []
                
            news_items = []
            for item in data["feed"][:limit]:
                # Format the time published
                time_str = item.get("time_published", "")
                try:
                    if time_str:
                        dt = datetime.datetime.strptime(time_str, "%Y%m%dT%H%M%S")
                        formatted_time = dt.strftime("%b %d, %Y at %H:%M")
                    else:
                        formatted_time = ""
                except:
                    formatted_time = time_str
                
                news_items.append({
                    "title": item.get("title", "No title"),
                    "url": item.get("url", ""),
                    "time_published": formatted_time,
                    "summary": item.get("summary", "No summary available"),
                    "source": item.get("source", "Unknown Source")
                })
                
            return news_items
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []