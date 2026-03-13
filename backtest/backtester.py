# backtest/backtester.py
import pandas as pd
from strategies.indicators import calculate_ema, calculate_rsi, calculate_atr

def calculate_historical_winrate(df):
    """
    Simulates a basic trend-following strategy on historical data
    to see if the asset behaves well with the strategy parameters.
    """
    close = df['Close']
    high = df['High']
    low = df['Low']
    
    ema20 = calculate_ema(df, 20)
    rsi14 = calculate_rsi(df, 14)
    atr = calculate_atr(df, 14)
    
    trades = 0
    wins = 0
    
    equity = pd.Series(1.0, index=df.index)
    
    in_position = False
    entry_price = 0
    stop_loss = 0
    target_price = 0
    
    for i in range(20, len(df)):
        if not in_position:
            # Entry condition at close of i-1
            if close.iloc[i-1] > ema20.iloc[i-1] and 40 <= rsi14.iloc[i-1] <= 70:
                in_position = True
                entry_price = close.iloc[i]
                current_atr = atr.iloc[i] if not pd.isna(atr.iloc[i]) else (entry_price * 0.03)
                stop_loss = entry_price - (2 * current_atr)
                target_price = entry_price + (4 * current_atr) # 1:2 RR
                trades += 1
            
            equity.iloc[i] = equity.iloc[i-1]
        else:
            if low.iloc[i] <= stop_loss:
                in_position = False
                equity.iloc[i] = equity.iloc[i-1] * (stop_loss / entry_price)
            elif high.iloc[i] >= target_price:
                in_position = False
                wins += 1
                equity.iloc[i] = equity.iloc[i-1] * (target_price / entry_price)
            else:
                equity.iloc[i] = equity.iloc[i-1]
                
    winrate = wins / trades if trades > 0 else 0
    return equity, winrate