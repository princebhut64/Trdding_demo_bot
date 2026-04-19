import time
from app.data import get_data
from app.strategy import apply_strategy, risk_management
from app.notifier import send

stocks = ["RELIANCE.BSE", "TCS.BSE", "INFY.BSE"]

def run():
    for stock in stocks:
        df = get_data(stock)

        if df is None:
            continue

        signal = apply_strategy(df)

        if signal != "HOLD":
            trade = risk_management(df)

            msg = f"""
📊 {stock}
Signal: {signal}
Price: {trade['price']}
Target: {trade['target']}
StopLoss: {trade['sl']}
"""
            print(msg)
            send(msg)

while True:
    run()
    time.sleep(300)
