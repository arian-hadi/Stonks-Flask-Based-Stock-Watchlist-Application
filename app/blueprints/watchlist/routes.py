from flask import Blueprint,render_template

watchlist_bp = Blueprint('watchlist_bp', __name__)

@watchlist_bp.route('/')
def watchlist():
    return render_template("watchlist.html")