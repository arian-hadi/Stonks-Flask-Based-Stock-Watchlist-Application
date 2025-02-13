from flask import Flask
from app.config import Config
from app.extension import init_extensions, scheduler
from app.blueprints.main.routes import main_bp
from app.blueprints.watchlist.routes import watchlist_bp,daily_stock_report
from app.blueprints.auth.routes import auth_bp
from app.blueprints.stock_detail.routes import stock_details_bp
from app.blueprints.auth.utils import load_user  # Import the user_loader function
from apscheduler.triggers.cron import CronTrigger
from extension import db

celery = None 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)

    app.register_blueprint(main_bp) 
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(stock_details_bp)

    with app.app_context():
        # Schedule the daily_stock_report task  

        db.create_all()

        scheduler.add_job(
            id='daily_stock_report',
            func=daily_stock_report,
            args=[app],  # Pass the app instance
            trigger=CronTrigger(hour=23),
            replace_existing=True
        )    

    return app
