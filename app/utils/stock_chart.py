import requests
import os
from flask import Blueprint



stock_details_bp = Blueprint('stock_details', __name__)

FINNHUB_API_KEY = os.getenv("FINNHUB_SECRET_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/quote"

def fetch_stock_details(symbol):
    """Fetch stock details from Finnhub for the details page."""
    response = requests.get(FINNHUB_URL, params={"symbol": symbol, "token": FINNHUB_API_KEY})
    data = response.json()

    if "c" not in data:
        return {"error": "Failed to fetch stock details"}

    return {
        "symbol": symbol,
        "current_price": data["c"],
        "change": data["d"],
        "percent_change": data["dp"],
        "high": data["h"],
        "low": data["l"],
        "open": data["o"],
        "previous_close": data["pc"],
    }

