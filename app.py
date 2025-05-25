"""
Streamlit web application for the stock analysis system.
"""

import streamlit as st
from src.orchestrator import StockAnalysisOrchestrator

# Set page configuration
st.set_page_config(
    page_title="Stock Analysis System",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
# Update the custom CSS section
st.markdown("""
<style>
    /* Dark theme styles */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    
    .main-header {
        font-size: 2.5rem;
        color: #60a5fa;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(45deg, #1e293b, #334155);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    .card {
        background: linear-gradient(45deg, #1e293b, #334155);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        border: 1px solid #475569;
    }
    
    .news-item {
        background: #1e293b;
        border-left: 4px solid #60a5fa;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 0 10px 10px 0;
        transition: transform 0.2s;
    }
    
    .news-item:hover {
        transform: translateX(5px);
    }
    
    .price-up {
        color: #4ade80;
        font-weight: bold;
    }
    
    .price-down {
        color: #f87171;
        font-weight: bold;
    }
    
    .ticker-symbol {
        font-size: 2.5rem;
        font-weight: bold;
        color: #60a5fa;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Style for example buttons */
    .stButton button {
        background: linear-gradient(45deg, #2563eb, #3b82f6);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Style for input box */
    .stTextInput input {
        background: #1e293b;
        border: 1px solid #475569;
        color: #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .stTextInput input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
    }
    
    /* Links styling */
    a {
        color: #60a5fa;
        text-decoration: none;
        transition: color 0.2s;
    }
    
    a:hover {
        color: #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# Update example queries to include Indian stocks
examples = [
    "How is Tata Motors stock performing?",
    "What's happening with Reliance stock?",
    "Analyze Infosys stock this week",
    "Why did Tesla stock drop today?",
    "HDFC Bank stock analysis"
]

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    return StockAnalysisOrchestrator()

orchestrator = get_orchestrator()

# Header
st.markdown('<div class="main-header">📈 Stock Analysis System</div>', unsafe_allow_html=True)
st.markdown("""
This system analyzes stocks based on your queries. Ask about recent price movements, 
news, and get AI-powered analysis of what's happening with any stock.
""")

# Example queries
st.markdown('<div class="sub-header">Example Queries</div>', unsafe_allow_html=True)
examples = [
    "Why did Tesla stock drop today?",
    "What's happening with Palantir stock recently?",
    "How has Nvidia stock changed in the last 7 days?",
    "Analyze Apple stock performance this week",
    "What's going on with Microsoft stock in the last month?"
]

# Create columns for example buttons
cols = st.columns(len(examples))
for i, col in enumerate(cols):
    if col.button(examples[i], key=f"example_{i}"):
        st.session_state.query = examples[i]

# Query input
query = st.text_input("Enter your stock query:", value=st.session_state.get("query", ""), key="stock_query")

# Process query
if query:
    with st.spinner("Analyzing stock data..."):
        response = orchestrator.process_query(query)
        
        if not response["success"]:
            st.error(response["message"])
        else:
            # Display ticker and current price
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f'<div class="ticker-symbol">{response["ticker"]}</div>', unsafe_allow_html=True)
            with col2:
                price_change_class = "price-up" if float(response["price"]["change_today"].strip("%")) >= 0 else "price-down"
                st.markdown(f"""
                <div class="card">
                    <h3>Current Price: ${response["price"]["current"]}</h3>
                    <p>Today's Change: <span class="{price_change_class}">{response["price"]["change_today"]}</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display price change
            st.markdown('<div class="sub-header">Price Change</div>', unsafe_allow_html=True)
            price_change = response["price_change"]
            change_class = "price-up" if float(price_change["percent_change"].strip("%")) >= 0 else "price-down"
            
            st.markdown(f"""
            <div class="card">
                <p>From {price_change["start_date"]} to {price_change["end_date"]} ({price_change["days"]} days):</p>
                <p>Starting Price: ${price_change["start_price"]}</p>
                <p>Ending Price: ${price_change["end_price"]}</p>
                <p>Change: <span class="{change_class}">${price_change["absolute_change"]} ({price_change["percent_change"]})</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display analysis
            st.markdown('<div class="sub-header">Analysis</div>', unsafe_allow_html=True)
            st.markdown(response["analysis"])  # No need for unsafe_allow_html=True for markdown
            
            # Display news
            st.markdown('<div class="sub-header">Recent News</div>', unsafe_allow_html=True)
            if response["news"]:
                for news in response["news"]:
                    st.markdown(f"""
                    <div class="news-item">
                        <h4>{news["title"]}</h4>
                        <p>{news["summary"]}</p>
                        <p><small>{news["time_published"]}</small></p>
                        <a href="{news["url"]}" target="_blank">Read more</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent news found for this stock.")

# Footer
st.markdown("---")
st.markdown("Built with Google ADK and Alpha Vantage API")