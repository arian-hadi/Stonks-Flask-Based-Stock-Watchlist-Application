from flask import Blueprint, render_template

signup_bp = Blueprint('signup_bp', __name__)
login_bp = Blueprint('login_bp', __name__)

@signup_bp.route('/signup')
def signup():
    return render_template("auth/signup.html")


@login_bp.route('/login')
def login():
    return render_template("auth/login.html")