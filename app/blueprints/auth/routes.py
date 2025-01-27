from flask import Blueprint, render_template, request,redirect, url_for,flash 
from app.forms import RegisterForm, LoginForm 
from app.extension import db
from app.models import User
from flask_login import login_user, logout_user,login_required


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('watchlist.watchlist'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/signup', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or email already taken. Please choose another.', 'warning')
            return render_template('auth/signup.html', form=form)
        
        # Create and save the new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))