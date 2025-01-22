from flask import Blueprint, render_template, request

watchlist_bp = Blueprint('watchlist', __name__)

# Store user stocks temporarily (in memory)
user_stocks = []

@watchlist_bp.route('/', methods=['GET', 'POST'])
def watchlist():
    stocks = ["AAPL", "GOOGL", "AMZN", "TSLA", "MSFT"]  # Predefined stock suggestions

    if request.method == "POST":
        new_stock = request.form.get("stock")
        if new_stock and new_stock not in user_stocks:  # Prevent duplicates
            user_stocks.append(new_stock)

    return render_template("watchlist.html", stocks=stocks, user_stocks=user_stocks)
