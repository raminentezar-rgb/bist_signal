# strategies/relative_strength.py

import pandas as pd

def relative_strength(df_stock, df_bist):
    """
    محاسبه قدرت نسبی سهم نسبت به شاخص.
    فرمول جدید: تفاوت بازدهی سهم و شاخص (Alpha)
    این روش در بازارهای منفی هم به درستی عمل می‌کند.
    """
    if df_stock is None or df_stock.empty or df_bist is None or df_bist.empty:
        return 0

    # اطمینان از اینکه Series هستند
    close_stock = df_stock['Close'].squeeze()
    close_bist = df_bist['Close'].squeeze()

    # محاسبه بازده ۶ ماهه (از ابتدای دیتا فریم تا انتها)
    ret_stock = (close_stock.iloc[-1] / close_stock.iloc[0]) - 1
    ret_bist = (close_bist.iloc[-1] / close_bist.iloc[0]) - 1

    # بازگرداندن تفاوت (Outperformance)
    # اگر مثبت باشد یعنی سهم از بازار بهتر عمل کرده است
    return ret_stock - ret_bist