import pandas as pd

def market_is_bullish(df_bist):

    close = df_bist['Close'].squeeze()

    ema50 = close.ewm(span=50, adjust=False).mean()

    last_price = close.iloc[-1]
    last_ema = ema50.iloc[-1]

    return last_price > last_ema