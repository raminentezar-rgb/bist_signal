import pandas as pd

def breakout_signal(df):

    if len(df) < 5:
        return False

    # مقاومت 3 روزه به جای 20 روزه
    resistance = df['High'].rolling(3).max().iloc[-2]

    price = df['Close'].iloc[-1]

    volume = df['Volume'].iloc[-1]
    avg_volume = df['Volume'].rolling(3).mean().iloc[-1]

    # شرط ساده‌تر: حجم فقط باید برابر میانگین باشد
    if price > resistance and volume >= avg_volume:
        return True

    return False