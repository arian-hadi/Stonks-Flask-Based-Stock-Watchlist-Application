# from flask import Blueprint, render_template, redirect, url_for
# from app.extension import db
# from app.forms import StockForm
# from app.models import Stock
# from flask_login import login_required,current_user
# from app.utils.finnhub_utils import get_stock_quote

# watchlist_bp = Blueprint('watchlist', __name__)
# @watchlist_bp.route('/', methods=['GET', 'POST'])
# @login_required
# def watchlist():
#     form = StockForm()
#     error = None

#     # Handle form submission for adding a stock
#     if form.validate_on_submit():
#         new_stock = form.stock.data.upper()
#         if new_stock:
#             # Check if the stock is already in the user's watchlist
#             existing_stock = Stock.query.filter_by(symbol=new_stock, user_id=current_user.id).first()
#             if not existing_stock:
#                 # Add stock to the user's watchlist
#                 stock = Stock(symbol=new_stock, user_id=current_user.id, is_global=False)  # User-specific stock
#                 db.session.add(stock)
#                 db.session.commit()
#         return redirect(url_for('watchlist.watchlist'))

#     # Retrieve the user's watchlist (user-specific stocks)
#     user_stocks = Stock.query.filter_by(user_id=current_user.id, is_global=False).all()

#     # Retrieve global stocks (predefined stocks for all users)
#     global_stocks = Stock.query.filter_by(is_global=True).all()

#     # Retrieve stock data for both user and global stocks
#     user_stock_data = [get_stock_quote(stock.symbol) for stock in user_stocks]
#     global_stock_data = [get_stock_quote(stock.symbol) for stock in global_stocks]

#     # Check for errors in retrieving stock data
#     if any(stock.get("error") for stock in user_stock_data + global_stock_data):
#         error = "Some stocks couldn't be retrieved. Please try again later."

#     return render_template(
#         "watchlist.html",
#         form=form,
#         stocks=user_stock_data,
#         user_stocks=user_stocks,
#         global_stocks=global_stock_data,
#         username=current_user.username,
#         error=error
#     )

from flask import Blueprint, render_template, redirect, url_for
from app.extension import db
from app.forms import AddStockForm, DeleteStockForm
from app.models import Stock
from flask_login import login_required,current_user
from app.utils.finnhub_utils import get_all_stock_quotes

watchlist_bp = Blueprint('watchlist', __name__)
@watchlist_bp.route('/', methods=['GET'])
@login_required
def watchlist():
    
    # Fetch 20 famous stocks from the API
    stock_data = get_all_stock_quotes()

    # Fetch user's added stocks from DB
    user_stocks = Stock.query.filter_by(user_id=current_user.id).all()
    user_symbols = {stock.symbol for stock in user_stocks}  

    add_form = AddStockForm()
    delete_form = DeleteStockForm()
    return render_template(
        "watchlist.html",
        stocks=stock_data,  
        user_stocks=user_symbols,  
        username=current_user.username,
        add_form=add_form,
        delete_form=delete_form
    )

@watchlist_bp.route('/add/<symbol>', methods=['POST'])
@login_required
def add_stock(symbol):
    form = AddStockForm()
    """Adds a stock to the user's watchlist."""
    if form.validate_on_submit():
        # Check if the stock is already in the user's watchlist
        if not Stock.query.filter_by(symbol=symbol, user_id=current_user.id).first():
            db.session.add(Stock(symbol=symbol, user_id=current_user.id))
            db.session.commit()
    return redirect(url_for('watchlist.watchlist'))

@watchlist_bp.route('/remove/<symbol>', methods=['POST'])
@login_required
def remove_stock(symbol):
    form = DeleteStockForm()
    """Removes a stock from the user's watchlist."""
    if form.validate_on_submit():
        stock = Stock.query.filter_by(symbol=symbol, user_id=current_user.id).first()
        if stock:
            db.session.delete(stock)
            db.session.commit()
    return redirect(url_for('watchlist.watchlist'))
