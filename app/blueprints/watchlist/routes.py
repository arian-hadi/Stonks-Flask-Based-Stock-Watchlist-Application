from flask import Blueprint, render_template, redirect, url_for, current_app
from app.extension import db
from app.forms import AddStockForm, DeleteStockForm
from app.models import Stock, Notification, User
from flask_login import login_required,current_user
from app.utils.finnhub_utils import get_all_stock_quotes, get_stock_quote
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
    """Send daily stock performance report to all users, skipping invalid emails and avoiding unnecessary API calls."""
    with app.app_context():
        users = User.query.all()
        for user in users:
            if not is_valid_email(user.email):
                print(f"Skipping invalid email: {user.email}")
                continue  # Skip this user if their email is invalid

            user_stocks = Stock.query.filter_by(user_id=user.id).all()
            if not user_stocks:
                print(f"No stocks in watchlist for user: {user.email}")
                continue  # Skip API calls if user has no stocks

            stock_report = ""
            for stock in user_stocks:
                stock_data = get_stock_quote(stock.symbol)
                stock_report += f"{stock.symbol}: ${stock_data['price']} ({stock_data['change_percent']}%)\n"

            send_report(user.email, stock_report)