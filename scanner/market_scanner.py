# scanner/market_scanner.py

import yfinance as yf
import pandas as pd
from symbols import BIST_SYMBOLS

BIST_INDEX = "XU100.IS"

def clean_dataframe(df):
    """تمیز کردن دیتافریم yfinance برای تک‌سهم"""
    if df is None or df.empty:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

def scan_market():
    signals = []

    # دانلود شاخص بازار
    try:
        df_bist_raw = yf.download(BIST_INDEX, period="6mo", progress=False, auto_adjust=True)
        df_bist = clean_dataframe(df_bist_raw)
    except Exception as e:
        print(f"Error downloading index: {e}")
        return signals

    if df_bist is None or len(df_bist) < 20:
        return signals

    # دانلود گروهی (Batch Download) برای جلوگیری از تداخل استخر تردها و مسدود شدن IP
    try:
        price_data = yf.download(
            BIST_SYMBOLS, 
            period="6mo", 
            progress=False, 
            auto_adjust=True, 
            group_by="ticker"
        )
    except Exception as e:
        print(f"Batch download failed: {e}")
        return signals

    if price_data.empty:
        return signals

    # بررسی تک‌تک سهم‌ها از فایل دانلود شده یکپارچه
    for symbol in BIST_SYMBOLS:
        if symbol in price_data:
            # Drop empty columns/rows if the stock was delisted or has no data
            df_stock = price_data[symbol].dropna(how="all")
            
            # پاکسازی نام ستون‌ها (در صورت لزوم)
            if isinstance(df_stock.columns, pd.MultiIndex):
                df_stock.columns = df_stock.columns.get_level_values(0)
            df_stock = df_stock.loc[:, ~df_stock.columns.duplicated()]

            # حداقل ۲۰ روز کاری دیتا برای محاسبه EMA20 لازم است
            if len(df_stock) > 20:
                signals.append({
                    "symbol": symbol,
                    "df": df_stock,
                    "df_bist": df_bist
                })

    return signals