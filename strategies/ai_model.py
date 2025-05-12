from .utils import fetch_current_prices

def generate_recommendations(user):
    prices = fetch_current_prices(user)
    actions = []

    # Rule-based logic
    for stock in user.stocks:
        price = prices.get(stock.stock_symbol, 0)
        if price > stock.purchase_price * 1.2:
            actions.append(f"Sell {stock.quantity} shares of {stock.stock_symbol}")
        elif price < stock.purchase_price * 0.9:
            actions.append(f"Buy 5 shares of {stock.stock_symbol}")
        else:
            actions.append(f"Hold {stock.stock_symbol}")

    for crypto in user.cryptos:
        price = prices.get(crypto.crypto_symbol, 0)
        if price > crypto.purchase_price * 1.2:
            actions.append(f"Sell {round(crypto.quantity * 0.5, 2)} {crypto.crypto_symbol}")
        elif price < crypto.purchase_price * 0.85:
            actions.append(f"Buy 0.1 {crypto.crypto_symbol}")
        else:
            actions.append(f"Hold {crypto.crypto_symbol}")

    for fund in user.mutual_funds:
        price = prices.get(fund.fund_symbol, 0)
        if price > fund.purchase_price * 1.15:
            actions.append(f"Sell {fund.quantity} units of {fund.fund_symbol}")
        else:
            actions.append(f"Hold {fund.fund_symbol}")

    return actions
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding
from extensions import db

# Step 1: Fetch all holdings for a specific user
def get_user_portfolio(user_id):
    stocks = StockHolding.query.filter_by(user_id=user_id).all()
    cryptos = CryptoHolding.query.filter_by(user_id=user_id).all()
    funds = MutualFundHolding.query.filter_by(user_id=user_id).all()
    return stocks, cryptos, funds

# Step 2: Convert to a unified portfolio vector
def build_portfolio_vector(user_id):
    stocks, cryptos, funds = get_user_portfolio(user_id)
    vector = {}

    for s in stocks:
        vector[s.stock_symbol] = {"quantity": s.quantity, "purchase_price": s.purchase_price}

    for c in cryptos:
        vector[c.crypto_symbol] = {"quantity": c.quantity, "purchase_price": c.purchase_price}

    for f in funds:
        vector[f.fund_symbol] = {"quantity": f.quantity, "purchase_price": f.purchase_price}

    return vector

# Step 3: Basic AI-driven recommendation logic (can be replaced with RL later)
def recommend_portfolio(user_id):
    portfolio = build_portfolio_vector(user_id)
    recommendations = []

    for asset, info in portfolio.items():
        qty = info["quantity"]
        purchase_price = info["purchase_price"]

        # Simple logic for now
        if qty < 2:
            recommendations.append({"action": "Buy", "amount": 1, "asset": asset})
        elif qty > 10:
            recommendations.append({"action": "Sell", "amount": 2, "asset": asset})
        else:
            recommendations.append({"action": "Hold", "amount": 0, "asset": asset})

    return recommendations
