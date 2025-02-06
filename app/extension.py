from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."
    mail.init_app(app)
    scheduler.start()
    app.scheduler = scheduler  