import requests
import os
from flask import Blueprint


# FINNHUB_API_KEY = os.getenv("FINNHUB_SECRET_KEY")
# FINNHUB_URL = "https://finnhub.io/api/v1/quote"

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

# def fetch_stock_details(symbol):
#     """Fetch stock details from Finnhub for the details page."""
#     response = requests.get(FINNHUB_URL, params={"symbol": symbol, "token": FINNHUB_API_KEY})
#     data = response.json()

#     if "c" not in data:
#         return {"error": "Failed to fetch stock details"}

#     return {
#         "symbol": symbol,
#         "current_price": data["c"],
#         "change": data["d"],
#         "percent_change": data["dp"],
#         "high": data["h"],
#         "low": data["l"],
#         "open": data["o"],
#         "previous_close": data["pc"],
#     }


def fetch_stock_history(symbol, time_period="week"):
    """Fetch stock historical data from Alpha Vantage (weekly or monthly)."""
    function = "TIME_SERIES_WEEKLY" if time_period == "week" else "TIME_SERIES_MONTHLY"
    
    response = requests.get(ALPHA_VANTAGE_URL, params={
        "function": function,
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    })
    
    data = response.json()
    
    time_series_key = "Weekly Time Series" if time_period == "week" else "Monthly Time Series"
    
    if time_series_key not in data:
        return {"error": f"Failed to fetch {time_period}ly stock history"}

    # Extract last week's or last month's data
    time_series = data[time_series_key]
    labels = list(time_series.keys())[:7]  # Last 7 days (week) or last 4 points (month)
    prices = [float(time_series[date]["4. close"]) for date in labels]

    return {"labels": labels[::-1], "prices": prices[::-1]}  # Reverse for correct order
