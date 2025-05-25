# 📈 Stock Analysis Multi-Agent System

Welcome to the **Stock Analysis Multi-Agent System**, a user-friendly tool that analyzes stocks using natural language queries. Powered by specialized AI agents, it delivers insights on stock prices, historical trends, and news, making stock analysis accessible to everyone! 🚀


# Demo Video of the application



https://github.com/user-attachments/assets/1cd3ed76-7f85-4744-b11e-713a82206932



## 🌟 Overview

This Python-based application processes queries like "Why did Tesla stock drop today?" to provide detailed stock analysis. It combines real-time data, news, and AI-driven insights through a modular multi-agent system, all wrapped in an intuitive Streamlit interface.

## 🎯 Key Features

- **Natural Language Queries**: Ask questions in plain English. 🗣️
- **Global Exchange Support**: Works with NYSE, NASDAQ, NSE, BSE, and more. 🌍
- **Timeframe Detection**: Extracts time periods (e.g., days, weeks) from queries. ⏳
- **Holistic Analysis**: Combines price data, news, and AI insights. 📊
- **Interactive Interface**: Clean, user-friendly web app built with Streamlit. 🖥️

## 🛠️ How It Works

The system uses a team of specialized agents, coordinated by an Orchestrator:

1. **Orchestrator**: Manages the workflow and delegates tasks. 🧠
2. **Identify Ticker Agent**: Extracts stock tickers (e.g., TSLA) using Gemini API. 🔍
3. **Ticker Price Agent**: Fetches current prices via Alpha Vantage API. 💰
4. **Ticker Price Change Agent**: Calculates price changes over time. 📉
5. **Ticker News Agent**: Collects recent news with summaries and links. 📰
6. **Ticker Analysis Agent**: Analyzes data and news for actionable insights. 📈

### Data Flow

1. Enter a query (e.g., "How’s Apple stock this month?").
2. The Orchestrator assigns tasks to agents.
3. Agents fetch ticker, price, historical data, and news.
4. The Analysis Agent generates insights.
5. Results are displayed via Streamlit. 🎉

## 🧑‍💻 Technologies Used

- **Python**: Core language. 🐍
- **Streamlit**: Web interface framework. 🌐
- **Alpha Vantage API**: Stock data and news. 📊
- **Google Gemini API**: Natural language processing. 🤖
- **Requests**: API communication. 🌐

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ 🐍
- API keys from Alpha Vantage and Google Gemini 🔑
- Python packages: `streamlit`, `requests`, etc. (see `requirements.txt`)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/stock-analysis-multi-agent.git
   cd stock-analysis-multi-agent
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**: Create a `.env` file:

   ```bash
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   GEMINI_API_KEY=your_gemini_key
   ```

4. **Run the App**:

   ```bash
   streamlit run app.py
   ```

5. **Access the App**: Visit `http://localhost:8501` in your browser. 🌐

## 📋 Usage

1. Open the Streamlit app.
2. Enter a query (e.g., "What’s Microsoft’s stock performance this week?").
3. View results, including:
   - Current price 💵
   - Price changes 📉
   - News articles 📰
   - AI insights 📊

## 📂 Project Structure

```
stock-analysis-multi-agent/
├── app.py                # Main Streamlit app
├── agents/               # Agent classes
│   ├── orchestrator.py
│   ├── identify_ticker.py
│   ├── ticker_price.py
│   ├── ticker_price_change.py
│   ├── ticker_news.py
│   ├── ticker_analysis.py
├── requirements.txt      # Dependencies
├── .env                  # API keys
└── README.md             # This file
```

## 🔧 Customization

- **New Exchanges**: Add support for more exchanges in `Ticker Price Agent`.
- **Advanced Analysis**: Enhance `Ticker Analysis Agent` with custom metrics.
- **UI Tweaks**: Customize Streamlit for new visualizations or themes.

## ⚠️ Limitations

- **API Limits**: Alpha Vantage has rate limits; monitor usage.
- **News Gaps**: Smaller stocks may have limited news coverage.
- **Query Parsing**: Complex queries may need rephrasing for accuracy.

## 🌟 Contributing

We’d love your contributions! To get started:

1. Fork the repo.
2. Create a branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push (`git push origin feature/your-feature`).
5. Open a pull request.

## 📬 Contact

Questions? Open a GitHub Issue or email jenithjain09@gmail.com.

## 🙏 Acknowledgments

- Alpha Vantage for stock data.
- Google Gemini for NLP.
- Streamlit for the web framework.

Happy analyzing! 📈
