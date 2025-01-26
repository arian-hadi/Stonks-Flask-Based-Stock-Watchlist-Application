from flask import Blueprint, render_template, request, redirect, url_for
from app.db_extension import db
from app.forms import StockForm
from app.models import Stock

watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route('/', methods=['GET', 'POST'])
def watchlist():
    form = StockForm()
    stocks = ["AAPL", "GOOGL", "AMZN", "TSLA", "MSFT"]  # Predefined stock suggestions

    if form.validate_on_submit():
        new_stock = form.stock.data.upper()  # Standardize stock symbols to uppercase
        if new_stock:
            existing_stock = Stock.query.filter_by(symbol=new_stock).first()
            if not existing_stock:
                stock = Stock(symbol=new_stock)  # Hardcoded user_id for now
                db.session.add(stock)
                db.session.commit()
        return redirect(url_for('watchlist.watchlist'))

    # Retrieve all saved stocks
    user_stocks = Stock.query.all()

    return render_template("watchlist.html", form=form, stocks=stocks, user_stocks=user_stocks)
