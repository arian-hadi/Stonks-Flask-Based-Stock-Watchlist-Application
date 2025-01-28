from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.finnhub_utils import get_stock_quote

stock_details_bp = Blueprint('stock_details', __name__)

@stock_details_bp.route('/stock/<symbol>', methods=['GET'])
@login_required
def stock_details(symbol):
    stock_data = get_stock_quote(symbol)
    if stock_data.get("error"):
        return render_template("stock_details.html", error=f"Unable to retrieve data for {symbol}.")
    
    return render_template("stock_details.html", stock=stock_data)
