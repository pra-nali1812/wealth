from flask import Blueprint, render_template
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding
from market_data.utils import get_stock_price, get_crypto_price, get_fund_price
from .utils import calculate_roi
from flask_login import login_required, current_user

performance_bp = Blueprint('performance', __name__)

@performance_bp.route('/performance')
@login_required
def view_performance():
    performance_data = []

    stocks = StockHolding.query.filter_by(user_id=current_user.id).all()
    cryptos = CryptoHolding.query.filter_by(user_id=current_user.id).all()
    funds = MutualFundHolding.query.filter_by(user_id=current_user.id).all()

    for stock in stocks:
        live = get_stock_price(stock.stock_symbol)
        price = float(live.get("05. price", 0))
        roi = calculate_roi(stock.purchase_price, price)
        performance_data.append({"symbol": stock.stock_symbol, "roi": roi})

    for crypto in cryptos:
        live = get_crypto_price(crypto.crypto_symbol)
        price = float(live.get("5. Exchange Rate", 0))
        roi = calculate_roi(crypto.purchase_price, price)
        performance_data.append({"symbol": crypto.crypto_symbol, "roi": roi})

    for fund in funds:
        live = get_fund_price(fund.fund_symbol)
        price = live.get("price", 0)
        roi = calculate_roi(fund.purchase_price, price)
        performance_data.append({"symbol": fund.fund_symbol, "roi": roi})

    return render_template('performance.html', performance_data=performance_data)
