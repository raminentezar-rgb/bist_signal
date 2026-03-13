import yfinance as yf

def download_data(symbol):


    df = yf.download(symbol, period="6mo", interval="1d")

    return df

