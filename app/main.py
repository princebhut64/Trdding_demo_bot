from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/webhook")
def webhook(data: dict):
    print("TradingView Alert:", data)
    return {"ok": True}
