"""
Orchestrator for the stock analysis multi-agent system.
"""

import re
from src.agents.identify_ticker import IdentifyTickerAgent
from src.agents.ticker_news import TickerNewsAgent
from src.agents.ticker_price import TickerPriceAgent
from src.agents.ticker_price_change import TickerPriceChangeAgent
from src.agents.ticker_analysis import TickerAnalysisAgent

class StockAnalysisOrchestrator:
    def __init__(self):
        self.identify_ticker_agent = IdentifyTickerAgent()
        self.ticker_news_agent = TickerNewsAgent()
        self.ticker_price_agent = TickerPriceAgent()
        self.ticker_price_change_agent = TickerPriceChangeAgent()
        self.ticker_analysis_agent = TickerAnalysisAgent()
        
    def _extract_timeframe(self, query):
        """
        Extract timeframe from query.
        
        Args:
            query (str): User query
            
        Returns:
            int: Number of days to look back
        """
        # Default timeframe
        timeframe = 7
        
        # Check for "today" or "yesterday"
        if re.search(r'\btoday\b', query, re.IGNORECASE):
            timeframe = 1
        elif re.search(r'\byesterday\b', query, re.IGNORECASE):
            timeframe = 2
        
        # Check for specific day mentions
        days_match = re.search(r'(\d+)\s*(day|days)', query, re.IGNORECASE)
        if days_match:
            timeframe = int(days_match.group(1))
            
        # Check for week mentions
        weeks_match = re.search(r'(\d+)\s*(week|weeks)', query, re.IGNORECASE)
        if weeks_match:
            timeframe = int(weeks_match.group(1)) * 7
            
        # Check for month mentions
        months_match = re.search(r'(\d+)\s*(month|months)', query, re.IGNORECASE)
        if months_match:
            timeframe = int(months_match.group(1)) * 30
            
        return timeframe
        
    def process_query(self, query):
        """
        Process a user query about stocks.
        
        Args:
            query (str): User's natural language query
            
        Returns:
            dict: Response with all relevant information
        """
        # Step 1: Identify ticker
        ticker = self.identify_ticker_agent.identify(query)
        if not ticker:
            return {
                "success": False,
                "message": "Could not identify a stock ticker in your query. Please specify a company name or ticker symbol."
            }
            
        # Step 2: Extract timeframe
        timeframe = self._extract_timeframe(query)
        
        # Step 3: Get current price
        price_data = self.ticker_price_agent.get_price(ticker)
        if not price_data:
            return {
                "success": False,
                "message": f"Could not retrieve price data for {ticker}. Please check if the ticker is correct."
            }
            
        # Step 4: Get price change
        price_change_data = self.ticker_price_change_agent.get_price_change(ticker, timeframe)
        if not price_change_data:
            return {
                "success": False,
                "message": f"Could not retrieve historical price data for {ticker}."
            }
            
        # Step 5: Get news
        news_data = self.ticker_news_agent.get_news(ticker)
        
        # Step 6: Generate analysis
        analysis = self.ticker_analysis_agent.analyze(ticker, price_data, news_data, price_change_data)
        
        # Step 7: Compile response
        response = {
            "success": True,
            "ticker": ticker,
            "query": query,
            "price": {
                "current": price_data["price"],
                "change_today": f"{price_data['change_percent']}%"
            },
            "price_change": {
                "days": timeframe,
                "start_date": price_change_data["past_date"],
                "end_date": price_change_data["latest_date"],
                "start_price": price_change_data["past_price"],
                "end_price": price_change_data["latest_price"],
                "absolute_change": price_change_data["absolute_change"],
                "percent_change": f"{price_change_data['percent_change']:.2f}%"
            },
            "news": news_data,
            "analysis": analysis
        }
        
        return response