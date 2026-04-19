import requests
import pandas as pd
from app.config import ALPHA_API_KEY

def get_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": ALPHA_API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    ts = data.get("Time Series (5min)", {})
    df = pd.DataFrame.from_dict(ts, orient="index")

    if df.empty:
        return None

    df.columns = ["open", "high", "low", "close", "volume"]
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)

    return df.sort_index()
