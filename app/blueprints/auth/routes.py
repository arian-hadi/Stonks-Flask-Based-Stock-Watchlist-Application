from flask import Blueprint, render_template, request,redirect, url_for
from app.forms import RegisterForm, LoginForm  


signup_bp = Blueprint('signup_bp', __name__)
login_bp = Blueprint('login_bp', __name__)

# @signup_bp.route('/signup', methods = ['GET', 'POST'])
# def signup():
#     return render_template("auth/signup.html")

# @login_bp.route('/login')
# def login():
#     return render_template("auth/login.html")

@login_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    #if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        #     login_user(user)
        #     redirect_url = request.args.get('next') or url_for('main.login')
        #     return redirect(redirect_url)
    #pass
    return render_template('auth/login.html', form=form)


# @main.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('main.index'))


@signup_bp.route('/signup', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form, csrf_enabled=True)
    #if form.validate_on_submit():
        # new_user = User(email=form.email.data,
        #         username=form.username.data,
        #         password=form.password.data)
        # # db.session.add(new_user)
        # # db.session.commit()
        # return redirect(url_for('login_bp.login'))
    return render_template('auth/signup.html', form=form)