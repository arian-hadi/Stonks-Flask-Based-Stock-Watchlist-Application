from flask import Blueprint, render_template, redirect, url_for
from app.extension import db
from app.forms import StockForm
from app.models import Stock
from flask_login import login_required,current_user
from app.blueprints.watchlist.finnhub_utils import get_stock_quote

watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route('/', methods=['GET', 'POST'])
@login_required
def watchlist():
    form = StockForm()
    #stocks = ["AAPL", "GOOGL", "AMZN", "TSLA", "MSFT"]
    error = None
    if form.validate_on_submit():
        new_stock = form.stock.data.upper()
        if new_stock:
            existing_stock = Stock.query.filter_by(symbol=new_stock, user_id=current_user.id).first()
            if not existing_stock:
                stock = Stock(symbol=new_stock, user_id=current_user.id)
                db.session.add(stock)
                db.session.commit()
        return redirect(url_for('watchlist.watchlist'))

    # Retrieve only the current user's stocks
    user_stocks = Stock.query.filter_by(user_id=current_user.id).all()
    stock_data = [get_stock_quote(stock.symbol) for stock in user_stocks]

    if any(stock.get("error") for stock in stock_data):
        error = "Some stocks couldn't be retrieved. Please try again later."

    return render_template("watchlist.html", form=form, stocks=stock_data, user_stocks=user_stocks,username = current_user.username, error=error)
