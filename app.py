import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("🚀 JAADUGAR PRO - Live Signals")

# Sidebar
st.sidebar.title("📈 Markets")
market = st.sidebar.selectbox("Select", ["Crypto 24/7", "NSE Stocks", "US Stocks"])

col1, col2 = st.columns([3,1])
with col1:
    symbol = st.text_input("Symbol", "BTC-USD")
with col2:
    if st.button("🔥 SIGNALS", type="primary"):
        with st.spinner("Fetching live data..."):
            try:
                # Data fetch
                data = yf.download(symbol, period="5d", interval="1h", progress=False)
                
                if len(data) > 14:  # Enough data for RSI
                    # RSI calculation FIXED
                    close = data['Close'].dropna()
                    delta = close.diff()
                    gain = delta.where(delta > 0, 0).fillna(0)
                    loss = -delta.where(delta < 0, 0).fillna(0)
                    
                    avg_gain = gain.rolling(window=14, min_periods=1).mean()
                    avg_loss = loss.rolling(window=14, min_periods=1).mean()
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                    current_rsi = rsi.iloc[-1]
                    
                    # Price change
                    change = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100
                    
                    # Signal logic
                    if current_rsi < 30 and change > 0:
                        signal, conf = "🚀 STRONG BUY", 85
                    elif current_rsi < 40:
                        signal, conf = "✅ BUY", 70
                    elif current_rsi > 70:
                        signal, conf = "📉 STRONG SELL", 80
                    elif current_rsi > 60:
                        signal, conf = "❌ SELL", 65
                    else:
                        signal, conf = "➡️ HOLD", 50

                    # Display results
                    st.header(f"**{signal}** ({conf}% Confidence)")
                    
                    colA, colB, colC = st.columns(3)
                    colA.metric("RSI", f"{current_rsi:.1f}")
                    colB.metric("Price Δ", f"{change:.2f}%")
                    colC.metric("Confidence", f"{conf}%")
                    
                    st.success(f"✅ {symbol} analyzed!")
                    
                else:
                    st.error("❌ Need more data. Try BTC-USD, RELIANCE.NS")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Quick picks
st.subheader("⭐ Quick Signals")
cols = st.columns(4)
if cols[0].button("BTC"): 
    st.session_state.symbol = "BTC-USD"
if cols[1].button("RELIANCE"): 
    st.session_state.symbol = "RELIANCE.NS"
if cols[2].button("NIFTY"): 
    st.session_state.symbol = "^NSEI"
if cols[3].button("AAPL"): 
    st.session_state.symbol = "AAPL"

st.info("💡 Crypto: BTC-USD | NSE: RELIANCE.NS, ^NSEI | US: AAPL")
