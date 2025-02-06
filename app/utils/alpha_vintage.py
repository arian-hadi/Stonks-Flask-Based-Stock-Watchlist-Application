import requests
import os


ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"


def fetch_stock_history(symbol, time_period="week"):
    function = "TIME_SERIES_WEEKLY" if time_period == "week" else "TIME_SERIES_MONTHLY"
    
    response = requests.get(ALPHA_VANTAGE_URL, params={
        "function": function,
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    })
    
    data = response.json()
    
    time_series_key = "Weekly Time Series" if time_period == "week" else "Monthly Time Series"
    
    if time_series_key not in data:
        print(f"API response: {data}")
        return {"error": f"Failed to fetch {time_period}ly stock history"}

    # Extract last week's or last month's data
    time_series = data[time_series_key]
    labels = list(time_series.keys())[:7]  
    prices = [float(time_series[date]["4. close"]) for date in labels]

    return {"labels": labels[::-1], "prices": prices[::-1]} 
