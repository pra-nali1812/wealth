# models.py
from extensions import db
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding

class InvestmentStrategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    risk_profile = db.Column(db.String(50), nullable=False)  # E.g., 'aggressive', 'balanced', 'conservative'
    allocations = db.Column(db.JSON, nullable=False)  # A dictionary for allocations, e.g., {'stock': 50, 'crypto': 30, 'fund': 20}

    def __repr__(self):
        return f'<InvestmentStrategy {self.risk_profile}>'
