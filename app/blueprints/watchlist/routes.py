from flask import Blueprint,render_template

watchlist_bp = Blueprint('watchlist_bp', __name__)

@watchlist_bp.route('/')
def watchlist():
    stocks = ["AAPL", "GOOGL", "AMZN", "TSLA", "MSFT"]
    return render_template("watchlist.html",stocks = stocks)

