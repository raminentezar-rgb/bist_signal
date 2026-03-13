import pandas as pd
import ta

def calculate_ema(df, period=20):
    """محاسبه EMA"""
    # مطمئن شو فقط Series به EMAIndicator میدی
    close_series = df['Close'].squeeze()  # squeeze تضمین می‌کنه 1D باشه
    ema_indicator = ta.trend.EMAIndicator(close=close_series, window=period)
    return ema_indicator.ema_indicator()

def calculate_rsi(df, period=14):
    """محاسبه RSI"""
    close_series = df['Close'].squeeze()  # squeeze تضمین می‌کنه 1D باشه
    rsi_indicator = ta.momentum.RSIIndicator(close=close_series, window=period)
    return rsi_indicator.rsi()

def detect_volume_spike(df, threshold=2):
    """شناسایی افزایش حجم غیرمعمول"""
    avg_vol = df['Volume'].rolling(20).mean()
    spike = df['Volume'] > (avg_vol * threshold)
    return spike

def calculate_atr(df, period=14):
    """محاسبه نزول واقعی میانگین (ATR)"""
    high = df['High'].squeeze()
    low = df['Low'].squeeze()
    close_series = df['Close'].squeeze()
    atr_indicator = ta.volatility.AverageTrueRange(high=high, low=low, close=close_series, window=period)
    return atr_indicator.average_true_range()