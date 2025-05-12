from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(500))
    risk_tolerance = db.Column(db.String(20), default='Medium')
    investment_goals = db.Column(db.Text)

    # Add these relationships 👇 if you have these models in your app
    stocks = db.relationship('StockHolding', backref='user', lazy=True)
    cryptos = db.relationship('CryptoHolding', backref='user', lazy=True)
    mutual_funds = db.relationship('MutualFundHolding', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
