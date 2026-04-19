import pandas as pd
from ta.momentum import RSIIndicator

def apply_strategy(df):
    if len(df) < 50:
        print(f"[WARNING] Not enough data for strategy ({len(df)} rows, need 50)")
        return "HOLD"

    # Work on a copy to avoid SettingWithCopyWarning
    df = df.copy()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()

    last = df.iloc[-1]

    # Check for NaN values in indicators
    if pd.isna(last['RSI']) or pd.isna(last['EMA20']) or pd.isna(last['EMA50']):
        print("[WARNING] Indicator values are NaN, not enough data")
        return "HOLD"

    if last['close'] > last['EMA20'] and last['close'] > last['EMA50'] and 55 < last['RSI'] < 70:
        return "BUY"

    elif last['RSI'] > 75 or last['close'] < last['EMA20']:
        return "SELL"

    return "HOLD"

def risk_management(df):
    last = df.iloc[-1]
    price = last['close']

    return {
        "price": round(price, 2),
        "target": round(price * 1.02, 2),
        "sl": round(price * 0.99, 2)
    }
