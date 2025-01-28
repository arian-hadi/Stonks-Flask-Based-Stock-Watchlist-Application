import requests
import os

FINNHUB_API_KEY = os.getenv("FINNHUB_SECRET_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/quote"

def get_stock_quote(symbol):
    try:
        response = requests.get(FINNHUB_URL, params={"symbol": symbol, "token": FINNHUB_API_KEY})
        data = response.json()

        # Check if the response contains an error or missing data
        if response.status_code != 200 or "c" not in data:
            raise ValueError("Invalid API response", )

        return {
            "symbol": symbol,
            "price": round(data["c"], 2),   # Current price
            "change_percent": round(data["dp"], 2),  # % Change
            "change_amount": round(data["d"], 2)  # Absolute Change
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")  # Log error for debugging
        return {"symbol": symbol, "price": "N/A", "change_percent": "N/A", "change_amount": "N/A", "error": True}
