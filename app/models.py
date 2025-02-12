from app.extension import db
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from datetime import datetime, timedelta, timezone
import random


bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    watchlist = db.relationship('Stock', backref='owner', lazy=True)
    password_hash = db.Column(db.String(255), nullable=False)
    reset_token = db.Column(db.String(255), nullable=True)  
    reset_token_expiry = db.Column(db.DateTime, nullable=True) 

    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.email, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, expiration=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt='password-reset-salt', max_age=expiration)
        except:
            return None
        return User.query.filter_by(email=email).first()
    
    def generate_otp(self):
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10)
        db.session.commit()

    def verify_otp(self, otp):
        return self.otp_code == otp and datetime.now(timezone.utc) < self.otp_expiry

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_global = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint('symbol', 'user_id', name='unique_stock_per_user'),
    )


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    last_notified = db.Column(db.DateTime, default=None)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    