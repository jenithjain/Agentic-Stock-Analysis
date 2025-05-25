"""
Agent for identifying stock tickers from natural language queries.
"""

import google.generativeai as genai
import requests
import re
from src.config.config import GEMINI_API_KEY, ALPHA_VANTAGE_API_KEY

class IdentifyTickerAgent:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        self.alpha_vantage_api_key = ALPHA_VANTAGE_API_KEY
        
        # Common stock tickers mapping (expanded with Indian stocks)
        self.common_tickers = {
            # Indian Stocks - Updated with correct tickers
            "tata motors": "TATAMOTORS.NS",
            "reliance industries": "RELIANCE.BO",  # Try BSE instead of NSE
            "reliance": "RELIANCE.BO",  # Try BSE instead of NSE
            "infosys": "INFY.NS",
            "tcs": "TCS.NS",
            "hdfc bank": "HDFCBANK.NS",
            "icici bank": "ICICIBANK.NS",
            "wipro": "WIPRO.NS",
            "bharti airtel": "BHARTIARTL.NS",
            "adani enterprises": "ADANIENT.NS",
            "sbi": "SBIN.NS",
            
            # US Stocks
            "tesla": "TSLA",
            "apple": "AAPL",
            "microsoft": "MSFT",
            "amazon": "AMZN",
            "google": "GOOGL",
            "alphabet": "GOOGL",
            "meta": "META",
            "facebook": "META",
            "nvidia": "NVDA",  # Make sure this is correct
            "palantir": "PLTR",
            "netflix": "NFLX",
            
            # Add more stocks as needed
        }
    
    def _verify_ticker(self, ticker):
        """
        Verify if a ticker is valid by making a test API call.
        
        Args:
            ticker (str): Ticker symbol to verify
            
        Returns:
            bool: True if ticker is valid, False otherwise
        """
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={self.alpha_vantage_api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            if "Global Quote" in data and data["Global Quote"] and "05. price" in data["Global Quote"]:
                return True
            return False
        except:
            return False
    
    def _search_ticker_symbol(self, company_name):
        """
        Search for a ticker symbol using Alpha Vantage API.
        
        Args:
            company_name (str): Company name to search for
            
        Returns:
            str: Best matching ticker symbol or None
        """
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={self.alpha_vantage_api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if "bestMatches" in data and data["bestMatches"]:
                # Return the best match ticker symbol
                ticker = data["bestMatches"][0]["1. symbol"]
                
                # Verify the ticker works
                if self._verify_ticker(ticker):
                    return ticker
                    
            return None
        except Exception as e:
            print(f"Error searching ticker: {e}")
            return None
    
    def identify(self, query):
        """
        Identify stock ticker from a natural language query.
        
        Args:
            query (str): User's natural language query
            
        Returns:
            str: Stock ticker symbol
        """
        # Step 1: Check if any common ticker names are in the query
        query_lower = query.lower()
        for company, ticker in self.common_tickers.items():
            if company in query_lower:
                # For Indian stocks, verify both NSE and BSE versions
                if ".NS" in ticker:
                    if self._verify_ticker(ticker):
                        return ticker
                    # Try BSE version if NSE fails
                    bse_ticker = ticker.replace(".NS", ".BO")
                    if self._verify_ticker(bse_ticker):
                        return bse_ticker
                elif ".BO" in ticker:
                    if self._verify_ticker(ticker):
                        return ticker
                    # Try NSE version if BSE fails
                    nse_ticker = ticker.replace(".BO", ".NS")
                    if self._verify_ticker(nse_ticker):
                        return nse_ticker
                else:
                    # For non-Indian stocks, just return the ticker
                    return ticker
        
        # Step 2: Check if there's already a ticker-like pattern in the query
        ticker_pattern = r'\b[A-Z]{1,5}\b'
        ticker_matches = re.findall(ticker_pattern, query)
        if ticker_matches:
            # Verify the ticker exists by making a test API call
            for potential_ticker in ticker_matches:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={potential_ticker}&apikey={self.alpha_vantage_api_key}"
                try:
                    response = requests.get(url)
                    data = response.json()
                    if "Global Quote" in data and data["Global Quote"] and "05. price" in data["Global Quote"]:
                        return potential_ticker
                except:
                    pass
        
        # Step 3: Try to extract company name and search for ticker
        # Extract potential company names using regex
        company_pattern = r'(?:about|on|for|with|how is|what\'s|whats|why did|why has|analyze)\s+([A-Za-z\s]+?)(?:\s+stock|\s+shares|\s+price|\s+company|\s+performance|$)'
        company_matches = re.findall(company_pattern, query_lower)
        
        if company_matches:
            for company_name in company_matches:
                company_name = company_name.strip()
                if len(company_name) > 2:  # Avoid too short matches
                    # Search for ticker using Alpha Vantage
                    ticker = self._search_ticker_symbol(company_name)
                    if ticker:
                        return ticker
        
        # Step 4: Use Gemini as a last resort
        prompt = f"""
        Extract the stock ticker symbol from this query: "{query}"
        If a company name is mentioned instead of a ticker, convert it to the appropriate ticker symbol.
        For Indian stocks, try both NSE (.NS) and BSE (.BO) extensions.
        
        Return ONLY the ticker symbol with no additional text or explanation.
        If no company or ticker is mentioned, return "UNKNOWN".
        """
        
        try:
            response = self.model.generate_content(prompt)
            ticker = response.text.strip().upper()
            
            if ticker == "UNKNOWN" or len(ticker) > 15:
                return None
                
            # For Indian stocks, verify both exchanges
            if ".NS" in ticker:
                if self._verify_ticker(ticker):
                    return ticker
                # Try BSE version
                bse_ticker = ticker.replace(".NS", ".BO")
                if self._verify_ticker(bse_ticker):
                    return bse_ticker
            elif ".BO" in ticker:
                if self._verify_ticker(ticker):
                    return ticker
                # Try NSE version
                nse_ticker = ticker.replace(".BO", ".NS")
                if self._verify_ticker(nse_ticker):
                    return nse_ticker
            
            # For other stocks, verify as is
            if self._verify_ticker(ticker):
                return ticker
                
            return None
        except Exception as e:
            print(f"Error extracting ticker with Gemini: {e}")
            return None