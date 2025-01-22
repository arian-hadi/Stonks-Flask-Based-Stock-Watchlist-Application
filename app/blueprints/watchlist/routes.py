from flask import Blueprint, render_template, request,redirect, url_for
from app.forms import StockForm

watchlist_bp = Blueprint('watchlist', __name__)

# Store user stocks temporarily (in memory)
user_stocks = []

@watchlist_bp.route('/', methods=['GET', 'POST'])
def watchlist():
    form = StockForm()
    stocks = ["AAPL", "GOOGL", "AMZN", "TSLA", "MSFT"]  # Predefined stock suggestions

    if form.validate_on_submit():
        new_stock = form.stock.data
        if new_stock and new_stock not in user_stocks:  # Prevent duplicates
            user_stocks.append(new_stock)
        return redirect(url_for('watchlist.watchlist'))  # Avoid form resubmission

    return render_template("watchlist.html", form=form, stocks=stocks, user_stocks=user_stocks)
