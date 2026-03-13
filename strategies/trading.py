# strategies/trading.py

import pandas as pd
from strategies.relative_strength import relative_strength
from strategies.indicators import calculate_ema, calculate_rsi, calculate_atr
from strategies.volume_spike import detect_volume_spike
from backtest.backtester import calculate_historical_winrate

def calculate_trade(df):
    """محاسبه Entry, Stop و Target بر اساس ATR"""
    entry = df['Close'].iloc[-1]
    
    atr = calculate_atr(df, 14).iloc[-1]
    if pd.isna(atr):
        atr = entry * 0.03
        
    # مدیریت سرمایه با استفاده از میانگین حرکت واقعی (ATR)
    # حد ضرر: 2 برابر ATR زیر قیمت ورود
    # حد سود: 4 برابر ATR بالای قیمت ورود (ریسک به ریوارد 1:2)
    stop = entry - (2 * atr)
    target = entry + (4 * atr)
    
    return entry, stop, target

def evaluate_signal(df, df_bist, min_rs=1.0, min_winrate=50, rsi_range=(40, 70), require_breakout=True, require_vol_spike=True):
    """
    ارزیابی و فیلتر کردن سیگنال بر اساس استراتژی و بازگرداندن اطلاعات ورود در صورت موفقیت
    """
    rs = relative_strength(df, df_bist)
    ema20 = calculate_ema(df, 20).iloc[-1]
    rsi14 = calculate_rsi(df, 14).iloc[-1]
    
    vol_spike = detect_volume_spike(df)
    # breakout checking: last close higher than max of previous 20 periods
    breakout = df['Close'].iloc[-1] > df['Close'].rolling(20).max().iloc[-2]
    
    last_close = df['Close'].iloc[-1]
    
    if require_vol_spike and not vol_spike:
        return None
    if require_breakout and not breakout:
        return None
        
    if rs < min_rs:
        return None
        
    if last_close < ema20:
        return None
        
    if not (rsi_range[0] <= rsi14 <= rsi_range[1]):
        return None
        
    entry, stop, target = calculate_trade(df)
    
    equity, winrate = calculate_historical_winrate(df)
    
    if winrate * 100 < min_winrate:
        return None
        
    return {
        "entry": entry,
        "stop": stop,
        "target": target,
        "rs": rs,
        "winrate": winrate * 100,
        "equity": equity
    }
