# dashboard/app.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from scanner.market_scanner import scan_market
from strategies.indicators import calculate_ema, calculate_rsi
from strategies.market_filter import market_is_bullish
from notifier.telegram_bot import send_telegram, send_chart
from strategies.trading import evaluate_signal


# -------------------------------
# Streamlit Setup
# -------------------------------
st.set_page_config(page_title="BIST Swing Trading Dashboard", layout="wide")
st.title("📊 BIST Ultra Swing Trading Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
min_rs = st.sidebar.slider("Min Relative Strength", 0.5, 2.0, 1.0)
min_winrate = st.sidebar.slider("Min WinRate %", 0, 100, 50)
rsi_min, rsi_max = st.sidebar.slider("RSI Range", 0, 100, (40, 70))

st.info("Scanning BIST Market...")

# -------------------------------
# Scan Market
# -------------------------------
signals = scan_market()

# اگر دیتایی دریافت نشد
if len(signals) == 0:
    st.warning("No market data available")
    st.stop()

# دریافت شاخص بازار
df_bist = signals[0]['df_bist']

# فیلتر روند بازار
if not market_is_bullish(df_bist):
    st.error("⚠️ Market Trend is BEARISH - No trading today")
    send_telegram("⚠️ Market Trend is BEARISH - No trading today")
    st.stop()


# -------------------------------
# Filter Signals
# -------------------------------
filtered_signals = []
all_equity = []

for signal in signals:
    symbol = signal['symbol']
    df = signal['df']

    try:
        result = evaluate_signal(df, df_bist, 
                                 min_rs=min_rs, 
                                 min_winrate=min_winrate, 
                                 rsi_range=(rsi_min, rsi_max), 
                                 require_breakout=True, 
                                 require_vol_spike=True)

        if not result:
            continue

        filtered_signals.append({
            "symbol": symbol,
            "entry": round(result['entry'], 2),
            "stop": round(result['stop'], 2),
            "target": round(result['target'], 2),
            "rs": round(result['rs'], 2),
            "winrate": round(result['winrate'], 2)
        })

        all_equity.append(result['equity'])


        # -------------------------------
        # Send Telegram message for this signal
        # -------------------------------
        msg = (
            f"📈 New Signal Detected!\n"
            f"Symbol: {symbol}\n"
            f"Entry: {entry:.2f}\n"
            f"Stop: {stop:.2f}\n"
            f"Target: {target:.2f}\n"
            f"RS: {rs:.2f}\n"
            f"WinRate: {winrate*100:.2f}%"
        )
        send_telegram(msg)
        send_chart(symbol, df)  # اگر میخوای نمودار هم به تلگرام بره

    except Exception as e:
        st.warning(f"⚠️ Skipped {symbol} due to error: {e}")


df_table = pd.DataFrame(filtered_signals)

# -------------------------------
# Streamlit UI
# -------------------------------
st.subheader("Filtered Signals")
st.dataframe(df_table)

# Candlestick + EMA + RSI Chart
st.subheader("Candlestick + EMA + RSI")
if not df_table.empty:
    selected_symbol = st.selectbox("Select Symbol to View Chart", df_table['symbol'])
    df_chart = next((s['df'] for s in signals if s['symbol'] == selected_symbol), None)

    if df_chart is not None:
        fig = go.Figure(data=[
            go.Candlestick(
                x=df_chart.index,
                open=df_chart['Open'],
                high=df_chart['High'],
                low=df_chart['Low'],
                close=df_chart['Close']
            )
        ])
        fig.add_trace(go.Scatter(x=df_chart.index, y=calculate_ema(df_chart,20), name='EMA20'))
        fig.add_trace(go.Scatter(x=df_chart.index, y=calculate_rsi(df_chart,14), name='RSI14', yaxis='y2'))

        fig.update_layout(
            yaxis2=dict(overlaying='y', side='right', title='RSI')
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No Signals")


# Equity Curve
if all_equity:
    combined_equity = pd.concat(all_equity, axis=1).fillna(1).prod(axis=1)
    fig_equity = go.Figure()
    fig_equity.add_trace(go.Scatter(x=combined_equity.index, y=combined_equity.values, name='Combined Equity Curve'))
    st.subheader("Combined Equity Curve - All Signals")
    st.plotly_chart(fig_equity, use_container_width=True)

# Daily Summary
total_signals = len(df_table)
total_profit = 0
if not df_table.empty:
    total_profit = sum((row['target']/row['entry'] - 1)*100 for _, row in df_table.iterrows())

st.subheader("Daily Summary")
st.markdown(
    f"""
- Total Signals: **{total_signals}**
- Potential Profit: **{total_profit:.2f}%**
"""
)