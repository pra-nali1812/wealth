from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding
from flask_login import login_required, current_user

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/add_stock', methods=['GET', 'POST'])
@login_required
def add_stock():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        quantity = request.form['quantity']
        purchase_price = request.form['purchase_price']
        new_stock = StockHolding(user_id=current_user.id, stock_symbol=stock_symbol, quantity=quantity, purchase_price=purchase_price)
        db.session.add(new_stock)
        db.session.commit()
        flash('Stock added successfully!')
        return redirect(url_for('portfolio.view_portfolio'))
    return render_template('add_stock.html')

@portfolio_bp.route('/add_crypto', methods=['GET', 'POST'])
@login_required
def add_crypto():
    if request.method == 'POST':
        crypto_symbol = request.form['crypto_symbol'].upper()
        quantity = float(request.form['quantity'])
        purchase_price = float(request.form['purchase_price'])
        new_crypto = CryptoHolding(user_id=current_user.id, crypto_symbol=crypto_symbol, quantity=quantity, purchase_price=purchase_price)
        db.session.add(new_crypto)
        db.session.commit()
        flash('Cryptocurrency added successfully!')
        return redirect(url_for('portfolio.view_portfolio'))
    return render_template('add_crypto.html')


@portfolio_bp.route('/add_fund', methods=['GET', 'POST'])
@login_required
def add_fund():
    if request.method == 'POST':
        fund_symbol = request.form['fund_symbol']
        quantity = float(request.form['quantity'])  # 🔥 convert to float
        purchase_price = float(request.form['purchase_price'])  # 🔥 convert to float

        new_fund = MutualFundHolding(
            user_id=current_user.id,
            fund_symbol=fund_symbol,
            quantity=quantity,
            purchase_price=purchase_price
        )
        db.session.add(new_fund)
        db.session.commit()
        flash('Mutual Fund added successfully!')
        return redirect(url_for('portfolio.view_portfolio'))
    return render_template('add_fund.html')


# @portfolio_bp.route('/view_portfolio')
# @login_required
# def view_portfolio():
#     stocks = StockHolding.query.filter_by(user_id=current_user.id).all()
#     cryptos = CryptoHolding.query.filter_by(user_id=current_user.id).all()
#     mutual_funds = MutualFundHolding.query.filter_by(user_id=current_user.id).all()
#     return render_template('view_portfolio.html', stocks=stocks, cryptos=cryptos, mutual_funds=mutual_funds)



from flask import render_template
from .models import StockHolding, CryptoHolding, MutualFundHolding
from market_data.utils import get_stock_price, get_crypto_price, get_fund_price

@portfolio_bp.route('/view_portfolio')
@login_required
def view_portfolio():
    stocks = StockHolding.query.filter_by(user_id=current_user.id).all()
    cryptos = CryptoHolding.query.filter_by(user_id=current_user.id).all()
    mutual_funds = MutualFundHolding.query.filter_by(user_id=current_user.id).all()

    live_prices = {}

    # Safely fetch live stock prices
    for stock in stocks:
        data = get_stock_price(stock.stock_symbol)
        price_str = data.get("05. price") if data else None
        try:
            live_prices[stock.stock_symbol] = float(price_str)
        except (TypeError, ValueError):
            live_prices[stock.stock_symbol] = None

    # Safely fetch live crypto prices
    for crypto in cryptos:
        data = get_crypto_price(crypto.crypto_symbol)
        price_str = data.get("5. Exchange Rate") if data else None
        try:
            live_prices[crypto.crypto_symbol] = float(price_str)
        except (TypeError, ValueError):
            live_prices[crypto.crypto_symbol] = None

    # Safely fetch live mutual fund prices
    for fund in mutual_funds:
        data = get_fund_price(fund.fund_symbol)
        price_str = data.get("price") if data else None
        try:
            live_prices[fund.fund_symbol] = float(price_str)
        except (TypeError, ValueError):
            live_prices[fund.fund_symbol] = None

    # === Calculate summary values ===
    def calculate_totals(items, symbol_getter):
        invested = 0
        current = 0
        for item in items:
            symbol = symbol_getter(item)
            live_price = live_prices.get(symbol)
            if live_price is not None:
                invested += item.quantity * item.purchase_price
                current += item.quantity * live_price
        return invested, current

    # Ensure proper return values (0, 0) if no holdings are found
    stock_invested, stock_current = calculate_totals(stocks, lambda x: x.stock_symbol)
    crypto_invested, crypto_current = calculate_totals(cryptos, lambda x: x.crypto_symbol)
    fund_invested, fund_current = calculate_totals(mutual_funds, lambda x: x.fund_symbol)

    total_invested = stock_invested + crypto_invested + fund_invested
    total_current = stock_current + crypto_current + fund_current
    total_gain_loss = total_current - total_invested

    return render_template(
        'view_portfolio.html',
        stocks=stocks,
        cryptos=cryptos,
        mutual_funds=mutual_funds,
        live_prices=live_prices,
        total_invested=total_invested,  # Ensure these variables are passed
        total_current=total_current,
        total_gain_loss=total_gain_loss
    )


from flask import redirect, url_for, flash
from .models import StockHolding, CryptoHolding, MutualFundHolding


# Delete stock
@portfolio_bp.route('/delete/stock/<int:stock_id>')
def delete_stock(stock_id):
    stock = StockHolding.query.get_or_404(stock_id)
    db.session.delete(stock)
    db.session.commit()
    flash("Stock deleted successfully.", "success")
    return redirect(url_for('portfolio.view_portfolio'))

# Delete crypto
@portfolio_bp.route('/delete/crypto/<int:crypto_id>')
def delete_crypto(crypto_id):
    crypto = CryptoHolding.query.get_or_404(crypto_id)
    db.session.delete(crypto)
    db.session.commit()
    flash("Crypto deleted successfully.", "success")
    return redirect(url_for('portfolio.view_portfolio'))

# Delete mutual fund
@portfolio_bp.route('/delete/fund/<int:fund_id>')
def delete_fund(fund_id):
    fund = MutualFundHolding.query.get_or_404(fund_id)
    db.session.delete(fund)
    db.session.commit()
    flash("Mutual fund deleted successfully.", "success")
    return redirect(url_for('portfolio.view_portfolio'))


@portfolio_bp.route('/add_asset', methods=['GET', 'POST'])
@login_required
def add_asset():
    if request.method == 'POST':
        asset_type = request.form['asset_type']
        symbol = request.form['symbol'].upper()
        quantity = float(request.form['quantity'])
        price = float(request.form['purchase_price'])

        if asset_type == 'stock':
            new_asset = StockHolding(user_id=current_user.id, stock_symbol=symbol, quantity=quantity, purchase_price=price)
        elif asset_type == 'crypto':
            new_asset = CryptoHolding(user_id=current_user.id, crypto_symbol=symbol, quantity=quantity, purchase_price=price)
        elif asset_type == 'mutual_fund':
            new_asset = MutualFundHolding(user_id=current_user.id, fund_symbol=symbol, quantity=quantity, purchase_price=price)
        else:
            flash('Invalid asset type selected.', 'danger')
            return redirect(url_for('portfolio.add_asset'))

        db.session.add(new_asset)
        db.session.commit()
        flash(f'{asset_type.replace("_", " ").title()} added successfully!', 'success')
        return redirect(url_for('portfolio.view_portfolio'))

    return render_template('add_asset.html')
