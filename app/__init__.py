from flask import Flask
 # Import the Blueprint
from app.blueprints.main.routes import main_bp
from app.blueprints.watchlist.routes import watchlist_bp
from app.blueprints.auth.routes import signup_bp, login_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    app.register_blueprint(main_bp) 
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist')
    app.register_blueprint(signup_bp, url_prefix='/auth')
    app.register_blueprint(login_bp,url_prefix = '/auth')
    return app
