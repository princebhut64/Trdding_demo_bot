import requests
from app.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send(msg):
    if TELEGRAM_TOKEN == "YOUR_TELEGRAM_TOKEN" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID":
        print("[WARNING] Telegram not configured, skipping notification")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg
        }, timeout=10)
        resp.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Telegram notification failed: {e}")
        return False
