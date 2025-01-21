from flask import Flask
from app.routes import routes  # Import the Blueprint

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(routes)  # Register the routes blueprint
    
    return app
