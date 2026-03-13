# strategies/relative_strength.py

import pandas as pd

def relative_strength(df_stock, df_bist):

    # اطمینان از اینکه Series هستند
    close_stock = df_stock['Close'].squeeze()
    close_bist = df_bist['Close'].squeeze()

    # محاسبه بازده
    ret_stock = (close_stock.iloc[-1] / close_stock.iloc[0]) - 1
    ret_bist = (close_bist.iloc[-1] / close_bist.iloc[0]) - 1

    # جلوگیری از تقسیم بر صفر
    if ret_bist == 0 or pd.isna(ret_bist):
        return 0

    rs = ret_stock / ret_bist

    return rs