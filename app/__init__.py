from flask import Flask
 # Import the Blueprint
from app.blueprints.main.routes import main_bp
from app.blueprints.watchlist.routes import watchlist_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(main_bp) 
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist') 
    return app
