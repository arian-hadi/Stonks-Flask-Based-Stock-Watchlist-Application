import requests
import os
from app.utils.stocks import STOCKS_DATA  # Import the stock list

FINNHUB_API_KEY = os.getenv("FINNHUB_SECRET_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/quote"

def get_stock_quote(symbol):
    try:
        response = requests.get(FINNHUB_URL, params={"symbol": symbol, "token": FINNHUB_API_KEY})
        data = response.json()

        
        if response.status_code != 200 or "c" not in data:
            raise ValueError(f"Invalid API response for {symbol}")

        return {
            "symbol": symbol,
            "price": round(data["c"], 2),  # Current price
            "change_percent": round(data["dp"], 2),  # % Change
            "change_amount": round(data["d"], 2),  # Absolute Change
        }

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")  
        return {"symbol": symbol, "price": "N/A", "change_percent": "N/A", "change_amount": "N/A", "error": True}

def get_all_stock_quotes():
    """Fetches stock data for the predefined 20 famous stocks."""
    stock_data = {}

    for symbol in STOCKS_DATA["all_stocks"].keys():
        stock_data[symbol] = get_stock_quote(symbol)

    return stock_data
