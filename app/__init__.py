from flask import Flask
from app.config import Config
from app.extension import db, migrate, init_extensions
from app.blueprints.auth.utils import load_user  # Ensures `user_loader` is properly registered
from app.blueprints.main.routes import main_bp
from app.blueprints.watchlist.routes import watchlist_bp
from app.blueprints.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)

    app.register_blueprint(main_bp) 
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app
