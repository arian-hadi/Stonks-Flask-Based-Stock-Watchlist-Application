import requests
import os
import time
from functools import lru_cache
from app.utils.stocks import STOCKS_DATA  # Import the stock list

FINNHUB_API_KEY = os.getenv("FINNHUB_SECRET_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/quote"


stock_cache = {}
CACHE_EXPIRY_TIME = 360  # Cache expiration time in seconds

def fetch_stock_quote(symbol):
    """Fetch stock data from Finnhub API."""
    try:
        response = requests.get(FINNHUB_URL, params={"symbol": symbol, "token": FINNHUB_API_KEY})
        data = response.json()

        if response.status_code != 200 or "c" not in data:
            raise ValueError(f"Invalid API response for {symbol}")

        return {
            "symbol": symbol,
            "price": round(data["c"], 2),
            "change_percent": round(data["dp"], 2),
            "change_amount": round(data["d"], 2),
            "high": round(data["h"], 2),
            "low": round(data["l"], 2),
            "open": round(data["o"], 2),
            "previous_close": round(data["pc"], 2),
        }
    
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return {"symbol": symbol, "price": "N/A", "change_percent": "N/A", "change_amount": "N/A", "error": True}


def get_stock_quote(symbol):
    """Fetch stock price with caching to avoid frequent API calls."""
    current_time = time.time()

    # Check if stock data is in cache and hasn't expired
    if symbol in stock_cache:
        cached_time, cached_data = stock_cache[symbol]
        if current_time - cached_time < CACHE_EXPIRY_TIME:
            return cached_data  # Return cached data if still valid

    # If not cached or expired, fetch new data
    stock_data = fetch_stock_quote(symbol)
    stock_cache[symbol] = (current_time, stock_data)  # Update cache

    return stock_data


def get_all_stock_quotes():
    """Fetch stock data for the predefined 20 famous stocks with caching."""
    stock_data = {}

    for symbol in STOCKS_DATA["all_stocks"].keys():
        stock_data[symbol] = get_stock_quote(symbol)

    return stock_data



def search_stock(symbol):
    """Search for a stock and return its latest data."""
    symbol = symbol.upper()

    # Check if stock is in the predefined list
    if symbol in STOCKS_DATA["all_stocks"]:
        return get_stock_quote(symbol)

    # If not in predefined stocks, fetch from API
    return get_stock_quote(symbol)