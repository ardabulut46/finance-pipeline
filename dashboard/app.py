import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Connect to DuckDB
DB_PATH = Path(__file__).parent.parent / "data" / "warehouse.duckdb"

@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH), read_only=True)

@st.cache_data
def load_data(query: str) -> pd.DataFrame:
    conn = get_connection()
    return conn.execute(query).fetchdf()

# Page config
st.set_page_config(page_title="Stock Analytics", page_icon="📈", layout="wide")
st.title("📈 Stock Analytics Dashboard")

# Sidebar - Stock selector
symbols = load_data("SELECT DISTINCT symbol FROM main.stg_stock_prices WHERE symbol != '^GSPC' ORDER BY symbol")
selected_stocks = st.sidebar.multiselect(
    "Select Stocks", 
    symbols['symbol'].tolist(),
    default=["AAPL", "MSFT", "NVDA"]
)

if not selected_stocks:
    st.warning("Please select at least one stock")
    st.stop()

# Build stock list for SQL
stock_list = ", ".join([f"'{s}'" for s in selected_stocks])

# Tab layout
tab1, tab2, tab3 = st.tabs(["📊 Price & Moving Averages", "🏆 Performance vs S&P 500", "🌡️ Volatility"])

with tab1:
    st.subheader("Price with Moving Averages")
    
    ma_data = load_data(f"""
        SELECT symbol, trade_date, close, ma_7, ma_30
        FROM main.mart_moving_averages
        WHERE symbol IN ({stock_list})
        ORDER BY symbol, trade_date
    """)
    
    for stock in selected_stocks:
        stock_df = ma_data[ma_data['symbol'] == stock]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_df['trade_date'], y=stock_df['close'], name='Close', line=dict(color='#00d4ff')))
        fig.add_trace(go.Scatter(x=stock_df['trade_date'], y=stock_df['ma_7'], name='MA 7', line=dict(color='#ff6b6b', dash='dot')))
        fig.add_trace(go.Scatter(x=stock_df['trade_date'], y=stock_df['ma_30'], name='MA 30', line=dict(color='#ffd93d', dash='dash')))
        fig.update_layout(title=stock, template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Daily Returns vs S&P 500")
    
    perf_data = load_data(f"""
        SELECT symbol, trade_date, daily_return_pct, sp500_return, alpha
        FROM main.mart_daily_performance
        WHERE symbol IN ({stock_list})
        ORDER BY trade_date DESC
        LIMIT 500
    """)
    
    # Summary table
    summary = load_data(f"""
        SELECT 
            symbol,
            ROUND(AVG(daily_return_pct), 3) AS avg_daily_return,
            ROUND(AVG(alpha), 3) AS avg_alpha,
            ROUND(SUM(alpha), 2) AS cumulative_alpha
        FROM main.mart_daily_performance
        WHERE symbol IN ({stock_list})
        GROUP BY symbol
        ORDER BY avg_alpha DESC
    """)
    
    st.dataframe(summary, use_container_width=True, hide_index=True)
    
    # Alpha chart
    fig = px.bar(summary, x='symbol', y='cumulative_alpha', color='cumulative_alpha',
                 color_continuous_scale=['#ff6b6b', '#ffd93d', '#51cf66'],
                 title='Cumulative Alpha (vs S&P 500)')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("30-Day Rolling Volatility")
    
    vol_data = load_data(f"""
        SELECT symbol, trade_date, volatility_30d, sector
        FROM main.mart_volatility
        WHERE symbol IN ({stock_list})
        ORDER BY trade_date
    """)
    
    fig = px.line(vol_data, x='trade_date', y='volatility_30d', color='symbol',
                  title='Volatility Over Time')
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Latest volatility by sector
    latest_vol = load_data("""
        SELECT symbol, sector, volatility_30d
        FROM main.mart_volatility
        WHERE trade_date = (SELECT MAX(trade_date) FROM main.mart_volatility)
        ORDER BY volatility_30d DESC
    """)
    
    st.subheader("Current Volatility by Stock")
    fig = px.bar(latest_vol, x='symbol', y='volatility_30d', color='sector',
                 title='Latest 30-Day Volatility')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)