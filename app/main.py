from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Trading Demo Bot")

class WebhookPayload(BaseModel):
    """Structured model for TradingView webhook alerts."""
    ticker: Optional[str] = None
    action: Optional[str] = None
    price: Optional[float] = None
    message: Optional[str] = None

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/webhook")
def webhook(data: WebhookPayload):
    print("TradingView Alert:", data.model_dump())
    return {"ok": True}
