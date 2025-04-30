import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from yfinance.exceptions import YFRateLimitError

st.set_page_config(page_title="📈 Stock Insights", layout="wide")

st.title("📊 Stock Market Dashboard")

# Input field
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, RELIANCE.NS)", "AAPL")

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    info = stock.info
    return hist, info

if ticker:
    try:
        hist, info = fetch_data(ticker)

        # Price Chart
        st.subheader(f"{ticker} - Price Chart (1 Year)")
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )])
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Financial Metrics
        st.subheader("🔎 Key Financial Metrics")
        metrics = {
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Volume": info.get("volume", "N/A"),
            "Book Value": info.get("bookValue", "N/A"),
            "P/B Ratio": info.get("priceToBook", "N/A"),
            "Beta": info.get("beta", "N/A"),
            "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
        }

        avg_52_week = (
            (info.get("fiftyTwoWeekHigh", 0) + info.get("fiftyTwoWeekLow", 0)) / 2
            if info.get("fiftyTwoWeekHigh") and info.get("fiftyTwoWeekLow")
            else "N/A"
        )
        metrics["52 Week Avg Price"] = avg_52_week

        for key, value in metrics.items():
            st.markdown(f"**{key}:** {value}")

    except YFRateLimitError:
        st.warning("⚠️ Yahoo Finance rate limit exceeded. Please try again later.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
