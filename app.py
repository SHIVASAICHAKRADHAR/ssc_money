import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Function to get stock data
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", start=start_date, end=end_date)
    return data

# Streamlit app layout
st.title('Stock Market Tracker')
st.sidebar.header('Stock Search')

# Sidebar Inputs
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))

# Fetch and display stock data
stock_data = get_stock_data(ticker, start_date, end_date)

# Display the stock data in a table
st.write("### Stock Data", stock_data)

# Plot stock data
st.write("### Stock Price Chart")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(stock_data.index, stock_data['Close'], label='Close Price')
ax.set_xlabel('Date')
ax.set_ylabel('Close Price (USD)')
ax.set_title(f'{ticker} Stock Price from {start_date} to {end_date}')
ax.legend()
st.pyplot(fig)
