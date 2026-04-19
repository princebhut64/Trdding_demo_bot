import time
import traceback
from app.data import get_data
from app.strategy import apply_strategy, risk_management
from app.notifier import send

stocks = ["RELIANCE.BSE", "TCS.BSE", "INFY.BSE"]

POLL_INTERVAL = 300  # seconds (5 minutes)

def run():
    for stock in stocks:
        try:
            df = get_data(stock)

            if df is None:
                continue

            signal = apply_strategy(df)

            if signal != "HOLD":
                trade = risk_management(df)

                msg = (
                    f"📊 {stock}\n"
                    f"Signal: {signal}\n"
                    f"Price: {trade['price']}\n"
                    f"Target: {trade['target']}\n"
                    f"StopLoss: {trade['sl']}"
                )
                print(msg)
                send(msg)
        except Exception as e:
            print(f"[ERROR] Failed processing {stock}: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    print("[INFO] Trading bot started")
    while True:
        try:
            run()
        except Exception as e:
            print(f"[ERROR] Unexpected error in main loop: {e}")
            traceback.print_exc()
        time.sleep(POLL_INTERVAL)
