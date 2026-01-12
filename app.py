import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Jaadugar Pro")
st.title("🚀 JAADUGAR PRO - Live Market Signals")

# Sidebar
st.sidebar.title("📈 Markets")
market = st.sidebar.selectbox("Select", ["Crypto 24/7", "NSE Stocks", "US Stocks"])

# Main input
col1, col2 = st.columns([3,1])
with col1:
    symbol = st.text_input("Symbol", "BTC-USD", key="main")
with col2:
    if st.button("🔥 SIGNALS", type="primary"):

        with st.spinner("Calculating..."):
            # Data fetch
            data = yf.download(symbol, period="5d", interval="1h", progress=False)
            
            if not data.empty:
                # RSI Calculate
                delta = data['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = -delta.where(delta < 0, 0).rolling(14).mean()
                rs = gain/loss
                rsi = 100 - (100/(1+rs)).iloc[-1]
                
                # Price change
                change = ((data['Close'].iloc[-1] - data['Close'].iloc[-2])/data['Close'].iloc[-2])*100
                
                # Signal Logic
                if rsi < 30 and change > 0:
                    signal, conf = "🚀 STRONG BUY", 85
                elif rsi < 40:
                    signal, conf = "✅ BUY", 70
                elif rsi > 70:
                    signal, conf = "📉 STRONG SELL", 80
                elif rsi > 60:
                    signal, conf = "❌ SELL", 65
                else:
                    signal, conf = "➡️ HOLD", 50

                # Results
                st.header(f"**{signal}** ({conf}% Confidence)")
                
                colA, colB, colC = st.columns(3)
                colA.metric("RSI", f"{rsi:.1f}")
                colB.metric("Price Δ", f"{change:.2f}%")
                colC.metric("Confidence", f"{conf}%")
                
                st.success(f"✅ {symbol} analyzed successfully!")
            else:
                st.error("❌ Invalid symbol! Try: BTC-USD, RELIANCE.NS, AAPL")

# Quick picks
st.subheader("⭐ Quick Test Symbols")
col1, col2, col3, col4 = st.columns(4)
if col1.button("BTC/USDT"): st.session_state.main = "BTC-USD"
if col2.button("RELIANCE"): st.session_state.main = "RELIANCE.NS" 
if col3.button("NIFTY"): st.session_state.main = "^NSEI"
if col4.button("AAPL"): st.session_state.main = "AAPL"

st.info("💡 **Crypto 24/7**: BTC-USD, ETH-USD\n**NSE**: RELIANCE.NS, ^NSEI\n**US**: AAPL, TSLA")
