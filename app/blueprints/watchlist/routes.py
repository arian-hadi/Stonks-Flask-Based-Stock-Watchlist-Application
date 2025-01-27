from flask import Blueprint, render_template, request, redirect, url_for
from app.extension import db
from app.forms import StockForm
from app.models import Stock
from flask_login import login_required,current_user

watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route('/', methods=['GET', 'POST'])
def watchlist():
    form = StockForm()
    stocks = ["AAPL", "GOOGL", "AMZN", "TSLA", "MSFT"]

    if form.validate_on_submit():
        new_stock = form.stock.data.upper()
        if new_stock:
            existing_stock = Stock.query.filter_by(symbol=new_stock, user_id=current_user.id).first()
            if not existing_stock:
                stock = Stock(symbol=new_stock, owner=current_user)
                db.session.add(stock)
                db.session.commit()
        return redirect(url_for('watchlist.watchlist'))

    # Retrieve only the current user's stocks
    user_stocks = Stock.query.filter_by(user_id=current_user.id).all()

    return render_template("watchlist.html", form=form, stocks=stocks, user_stocks=user_stocks)
