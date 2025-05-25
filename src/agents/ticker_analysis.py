"""
Agent for analyzing stock price movements based on news and price data.
"""

import google.generativeai as genai
from src.config.config import GEMINI_API_KEY

class TickerAnalysisAgent:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        
    def analyze(self, ticker, price_data, news_data, price_change_data):
        """
        Analyze stock price movements using news and price data.
        
        Args:
            ticker (str): Stock ticker symbol
            price_data (dict): Current price information
            news_data (list): Recent news articles
            price_change_data (dict): Price change information
            
        Returns:
            str: Analysis of price movements
        """
        # Format news for the prompt
        news_text = ""
        for i, news in enumerate(news_data):
            news_text += f"{i+1}. {news['title']} - {news['time_published']}\n"
            news_text += f"   Summary: {news['summary']}\n\n"
        
        # Determine currency symbol based on ticker suffix
        currency_symbol = "$"
        if ".NS" in ticker or ".BO" in ticker:
            currency_symbol = "₹"
        elif ".DE" in ticker or ".PA" in ticker or ".AMS" in ticker:
            currency_symbol = "€"
        elif ".L" in ticker:
            currency_symbol = "£"
        
        # Create prompt for Gemini
        prompt = f"""
        Analyze the recent price movements of {ticker} stock based on the following data:
        
        PRICE DATA:
        Current Price: {currency_symbol}{price_data['price']}
        Daily Change: {price_data['change_percent']}%
        
        PRICE CHANGE OVER {price_change_data['days']} DAYS:
        Price on {price_change_data['latest_date']}: {currency_symbol}{price_change_data['latest_price']}
        Price on {price_change_data['past_date']}: {currency_symbol}{price_change_data['past_price']}
        Change: {currency_symbol}{price_change_data['absolute_change']} ({price_change_data['percent_change']:.2f}%)
        
        RECENT NEWS:
        {news_text}
        
        Based on this information, provide a comprehensive analysis of:
        1. The likely reasons for the stock's recent price movements
        2. How news events may have influenced the stock price
        3. A brief outlook based on the current news and price trends
        4. Any relevant market context (industry trends, competitor performance, etc.)
        5. Any regional economic factors that might be affecting this stock
        
        Format your response in the following structure:
        
        # Summary
        (Provide a brief 2-3 sentence summary of the overall situation)
        
        # Price Movement Analysis
        (Analyze the reasons behind recent price changes)
        
        # News Impact
        (Explain how news events have influenced the stock)
        
        # Market Context
        (Provide relevant industry and market context)
        
        # Future Outlook
        (Provide a brief outlook based on current trends)
        
        Use bullet points for key insights where appropriate.
        Keep your analysis factual, balanced, and focused on explaining the relationship between news and price movements.
        """
        
        try:
            response = self.model.generate_content(prompt)
            raw_analysis = response.text
            
            # Return markdown-formatted text instead of HTML
            # This will render properly in Streamlit
            formatted_analysis = self._format_analysis_for_markdown(raw_analysis, ticker, price_data, price_change_data, currency_symbol)
            return formatted_analysis
        except Exception as e:
            print(f"Error generating analysis: {e}")
            return "Unable to generate analysis at this time."
    
    def _format_analysis_for_markdown(self, analysis_text, ticker, price_data, price_change_data, currency_symbol="$"):
        """
        Format the analysis text with Markdown for better display in Streamlit.
        
        Args:
            analysis_text (str): Raw analysis from Gemini
            ticker (str): Stock ticker symbol
            price_data (dict): Current price information
            price_change_data (dict): Price change information
            currency_symbol (str): Currency symbol to use
            
        Returns:
            str: Markdown-formatted analysis
        """
        # Determine if the stock is up or down
        price_change = float(price_data['change_percent'])
        price_direction = "📈" if price_change >= 0 else "📉"
        
        # Create a header with stock performance summary
        header = f"""
## {ticker} Stock Analysis {price_direction}

**Current Price:** {currency_symbol}{price_data['price']} ({price_data['change_percent']}%)

**{price_change_data['days']}-Day Change:** {currency_symbol}{price_change_data['absolute_change']} ({price_change_data['percent_change']:.2f}%)

---
"""
        
        # Combine header and analysis
        full_analysis = f"{header}\n{analysis_text}"
        
        return full_analysis