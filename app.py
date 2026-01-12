import streamlit as st
import yfinance as yf

st.set_page_config(layout="wide")
st.title("🚀 JAADUGAR PRO - NO ERROR VERSION")

# Sidebar
st.sidebar.title("📈 Markets")
market = st.sidebar.selectbox("Select", ["Crypto 24/7", "NSE Stocks", "US Stocks"])

col1, col2 = st.columns([3,1])
with col1:
    symbol = st.text_input("Symbol", "BTC-USD", key="symbol")
with col2:
    if st.button("🔥 LIVE SIGNALS", type="primary"):
        with st.spinner("Analyzing..."):
            try:
                # Simple data fetch
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="5d")
                
                if 'currentPrice' in info:
                    price = info['currentPrice']
                    change = info.get('regularMarketChangePercent', 0)
                    
                    # Super simple signal (no complex pandas)
                    if change > 2:
                        signal = "🚀 STRONG BUY"
                        conf = 80
                    elif change > 0:
                        signal = "✅ BUY" 
                        conf = 65
                    elif change < -2:
                        signal = "📉 STRONG SELL"
                        conf = 75
                    elif change < 0:
                        signal = "❌ SELL"
                        conf = 60
                    else:
                        signal = "➡️ HOLD"
                        conf = 50
                    
                    # Results
                    st.header(f"**{signal}** ({conf}% Confidence)")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Price", f"₹{price:.2f}")
                    col2.metric("Change", f"{change:.2f}%")
                    col3.metric("Confidence", f"{conf}%")
                    
                    st.success(f"✅ {symbol} LIVE analysis complete!")
                    
                else:
                    st.error("❌ Try: BTC-USD, RELIANCE.NS, AAPL")
                    
            except:
                st.error("❌ Invalid symbol! Try BTC-USD")

# Quick buttons
st.subheader("⭐ ONE-CLICK SIGNALS")
col1, col2, col3, col4 = st.columns(4)
if col1.button("🔥 BTC"): st.session_state.symbol = "BTC-USD"
if col2.button("📈 RELIANCE"): st.session_state.symbol = "RELIANCE.NS"
if col3.button("📊 NIFTY"): st.session_state.symbol = "^NSEI"
if col4.button("💰 AAPL"): st.session_state.symbol = "AAPL"

st.info("💡 **Crypto**: BTC-USD (24/7)\n**NSE**: RELIANCE.NS, ^NSEI\n**US**: AAPL")
