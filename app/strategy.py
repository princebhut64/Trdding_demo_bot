from ta.momentum import RSIIndicator

def apply_strategy(df):
    df['EMA20'] = df['close'].ewm(span=20).mean()
    df['EMA50'] = df['close'].ewm(span=50).mean()
    df['RSI'] = RSIIndicator(df['close']).rsi()

    last = df.iloc[-1]

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
