from flask import Blueprint, render_template, request,redirect, url_for,flash 
from app.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm,DeleteAccountForm
from app.extension import db
from app.models import User,Notification,Stock
from app.utils.email import send_reset_email, send_otp_email
from flask_login import login_user, logout_user,login_required, current_user
from datetime import datetime, timedelta, timezone


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            form.password.errors.append("Invalid password")  # Show error under password field
            return render_template('auth/login.html', form=form)


        if not user.is_verified:
            flash('Please verify your account using the OTP sent to your email.', 'warning')
            return redirect(url_for('auth.verify_otp', user_id=user.id))  # Redirect to OTP verification page
        
        
        login_user(user)
        return redirect(url_for('watchlist.watchlist'))

    return render_template('auth/login.html', form=form)



@auth_bp.route('/signup', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if the username or email is already taken
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()

        if existing_user:
            if existing_user.username == form.username.data:
                form.username.errors.append("This username is already taken.")
            if existing_user.email == form.email.data:
                form.email.errors.append("This email is already registered.")
            return render_template('auth/signup.html', form=form)  # Return form with errors

        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        user.generate_otp()
        send_otp_email(user.email, user.otp_code)

        # flash('Registration successful. Please log in.', 'success')
        # return redirect(url_for('auth.login'))
        flash('An OTP has been sent to your email.', 'info')
        return redirect(url_for('auth.verify_otp', user_id=user.id))

    return render_template('auth/signup.html', form=form)


@auth_bp.route('/verify_otp/<int:user_id>', methods=['GET', 'POST'])
def verify_otp(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        otp = request.form.get('otp')
        if user.verify_otp(otp):
            user.is_verified = True  # ✅ Mark as verified
            db.session.commit()
            flash('Your account has been verified. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired OTP.', 'danger')
    return render_template('auth/verify_otp.html', user_id=user.id)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_bp.homepage'))  # Use 'main_bp.homepage' to reference the Blueprint route


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
            return redirect(url_for('auth.forgot_password_sent'))
        else:
            flash("No account found with this email.", "danger")

    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user or user.reset_token_expiry.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        flash("Invalid or expired token.", "danger")
        return redirect(url_for('auth.reset_password_failed')) 

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        flash("Your password has been reset! You can now log in.", "success")
        return redirect(url_for('auth.reset_password_success'))

    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/forgot-password-sent')
def forgot_password_sent():
    return render_template('auth/forgot_password_sent.html')

@auth_bp.route('/reset-password-success')
def reset_password_success():
    return render_template('auth/reset_password_success.html')

@auth_bp.route('/reset-password-failed')
def reset_password_failed():
    return render_template('auth/reset_password_failed.html')


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):  # Verify password
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('auth.delete_account'))  

        user = User.query.get_or_404(current_user.id)

        # Delete related records
        Stock.query.filter_by(user_id=user.id).delete()
        Notification.query.filter_by(user_id=user.id).delete()

        # Delete user account
        db.session.delete(user)
        db.session.commit()

        # Log out the user
        logout_user()

        flash("Your account has been deleted successfully.", "success")
        return redirect(url_for('auth.account_deleted'))  # Redirect to success page

    return render_template('auth/delete_account.html', form=form)


@auth_bp.route('/account-deleted')
def account_deleted():
    return render_template('auth/account_deleted.html')


@auth_bp.route('/change-username', methods=['POST'])
@login_required
def change_username():
    new_username = request.form.get("new_username").strip()

    if not new_username:
        flash("Username cannot be empty.", "danger")
        return redirect(url_for('profile_page'))

    if new_username == current_user.username:
        flash("This is already your username.", "warning")
        return redirect(url_for('auth.profile'))

    # Check if the username is taken
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user:
        flash("This username is already taken. Choose another.", "danger")
        return redirect(url_for('profile_page'))

    # Update username
    current_user.username = new_username
    db.session.commit()

    flash("Username updated successfully!", "success")
    return redirect(url_for('auth.profile'))
