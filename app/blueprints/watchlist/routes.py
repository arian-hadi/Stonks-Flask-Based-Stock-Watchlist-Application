from flask import Blueprint, render_template, redirect, url_for, current_app, jsonify, request
from app.extension import db
from app.forms import AddStockForm, DeleteStockForm
from app.models import Stock, Notification, User
from flask_login import login_required,current_user
from app.utils.finnhub_utils import get_all_stock_quotes, get_stock_quote, search_stock
from app.extension import scheduler
from app.utils.email import send_report,is_valid_email
from apscheduler.triggers.cron import CronTrigger

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

            new_notification = Notification(user_id=current_user.id, stock_symbol=symbol, last_notified=None)
            db.session.add(new_notification)
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

            notification = Notification.query.filter_by(user_id=current_user.id, stock_symbol=symbol).first()
            if notification:
                db.session.delete(notification)
                db.session.commit()

    return redirect(url_for('watchlist.watchlist'))


# def daily_stock_report(app):
#     """Send daily stock performance report to all users."""
#     with app.app_context():
#         users = User.query.all()
#         for user in users:
#             user_stocks = Stock.query.filter_by(user_id=user.id).all()
#             stock_report = ""
#             for stock in user_stocks:
#                 stock_data = get_stock_quote(stock.symbol)
#                 stock_report += f"{stock.symbol}: ${stock_data['price']} ({stock_data['change_percent']}%)\n"
#             send_report(user.email, stock_report)

def daily_stock_report(app):
    with app.app_context():
        users = User.query.all()
        for user in users:
            if not is_valid_email(user.email):
                continue

            user_stocks = Stock.query.filter_by(user_id=user.id).all()
            if not user_stocks:
                continue

            stock_report = "Symbol   Price ($)   Change (%)   Change ($)   High   Low\n"
            stock_report += "-" * 60 + "\n"

            for stock in user_stocks:
                stock_data = get_stock_quote(stock.symbol)
                stock_report += (
                    f"{stock.symbol:<8} {stock_data['price']:<10} {stock_data['change_percent']:<10}% "
                    f"{stock_data['change_amount']:<10} {stock_data['high']:<6} {stock_data['low']:<6}\n"
                )

            send_report(user.email, stock_report)


@watchlist_bp.route('/search_stock', methods=['GET'])
@login_required
def search_stock_api():
    """Search for stocks based on user input."""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])  # Return empty list if query is empty

    stock_results = search_stock(query)  # Get matching stocks
    return jsonify(stock_results)