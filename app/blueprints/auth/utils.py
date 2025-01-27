from app.models import User
from app.extension import login_manager

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(user_id)