from flask import Blueprint, render_template, request,redirect, url_for,flash 
from app.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.extension import db
from app.models import User
from app.utils.email import send_reset_email
from flask_login import login_user, logout_user,login_required
from datetime import datetime, timedelta, timezone


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
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


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.generate_reset_token()
            user.reset_token = token
            user.reset_token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
            db.session.commit()

            reset_url = url_for('auth.reset_password', token=token, _external=True)
            send_reset_email(user.email, reset_url)

            flash("An email has been sent with instructions to reset your password.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("No account found with this email.", "danger")

    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user or user.reset_token_expiry.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        flash("Invalid or expired token.", "danger")
        return redirect(url_for('forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        flash("Your password has been reset! You can now log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)

