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

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed for {symbol}: {e}")
        return None
    except ValueError:
        print(f"[ERROR] Invalid JSON response for {symbol}")
        return None

    # Check for API error messages (rate limit, invalid key, etc.)
    if "Error Message" in data:
        print(f"[ERROR] Alpha Vantage error for {symbol}: {data['Error Message']}")
        return None
    if "Note" in data:
        print(f"[WARNING] Alpha Vantage rate limit: {data['Note']}")
        return None

    ts = data.get("Time Series (5min)", {})
    if not ts:
        print(f"[WARNING] No time series data for {symbol}")
        return None

    df = pd.DataFrame.from_dict(ts, orient="index")

    if df.empty:
        return None

    # Alpha Vantage column names have numeric prefixes like "1. open"
    df.columns = [col.split(". ", 1)[-1] if ". " in col else col for col in df.columns]

    expected_cols = ["open", "high", "low", "close", "volume"]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        print(f"[ERROR] Missing columns for {symbol}: {missing}. Got: {list(df.columns)}")
        return None

    df = df[expected_cols]
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)

    return df.sort_index()
