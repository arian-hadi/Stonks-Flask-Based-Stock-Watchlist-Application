from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from app.extension import db, migrate
 # Import the Blueprint
from app.blueprints.main.routes import main_bp
from app.blueprints.watchlist.routes import watchlist_bp
from app.blueprints.auth.routes import auth_bp


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        from app.models import User, Stock  # Import your models here
        db.create_all()  # Ensure tables are created



    app.register_blueprint(main_bp) 
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app
