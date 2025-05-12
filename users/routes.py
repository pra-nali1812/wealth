# users/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import db, login_manager
from users.models import User
from users.utils import login_current_user, logout_current_user
from flask_login import login_required, current_user
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding

users_bp = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('users.register'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully')
        return redirect(url_for('users.login'))
    return render_template('register.html')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_current_user(user)
            return redirect(url_for('users.dashboard'))  # ✅ Redirect to dashboard
        flash('Invalid credentials')
    return render_template('login.html')

@users_bp.route('/logout')
@login_required
def logout():
    logout_current_user()
    return redirect(url_for('users.login'))

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Update risk tolerance and goals
        current_user.risk_tolerance = request.form.get('risk_tolerance')
        current_user.investment_goals = request.form.get('investment_goals')

        # Update password if provided
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        if current_user.check_password(current_password):
            current_user.set_password(new_password)
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        else:
            flash('Incorrect current password.', 'danger')
            return redirect(url_for('users.profile'))

        db.session.commit()
        return redirect(url_for('users.profile'))

    return render_template('profile.html', user=current_user)


from flask import render_template
from flask_login import login_required, current_user
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding
from market_data.utils import get_stock_price, get_crypto_price, get_fund_price
from strategies.optimizer import simple_ai_recommendation
from performance.utils import calculate_roi

@users_bp.route('/dashboard')
@login_required
def dashboard():
    holdings = []
    performance_data = []
    live_prices = {}

    stocks = StockHolding.query.filter_by(user_id=current_user.id).all()
    cryptos = CryptoHolding.query.filter_by(user_id=current_user.id).all()
    funds = MutualFundHolding.query.filter_by(user_id=current_user.id).all()

    for s in stocks:
        price_info = get_stock_price(s.stock_symbol)
        price = float(price_info.get("05. price", 0))
        roi = calculate_roi(s.purchase_price, price)
        holdings.append({"symbol": s.stock_symbol, "quantity": s.quantity, "purchase_price": s.purchase_price})
        performance_data.append({"symbol": s.stock_symbol, "roi": roi})
        live_prices[s.stock_symbol] = price

    for c in cryptos:
        price_info = get_crypto_price(c.crypto_symbol)
        price = float(price_info.get("5. Exchange Rate", 0))
        roi = calculate_roi(c.purchase_price, price)
        holdings.append({"symbol": c.crypto_symbol, "quantity": c.quantity, "purchase_price": c.purchase_price})
        performance_data.append({"symbol": c.crypto_symbol, "roi": roi})
        live_prices[c.crypto_symbol] = price

    for f in funds:
        price_info = get_fund_price(f.fund_symbol)
        price = price_info.get("price", 0)
        roi = calculate_roi(f.purchase_price, price)
        holdings.append({"symbol": f.fund_symbol, "quantity": f.quantity, "purchase_price": f.purchase_price})
        performance_data.append({"symbol": f.fund_symbol, "roi": roi})
        live_prices[f.fund_symbol] = price

    suggestions = simple_ai_recommendation(holdings, live_prices)

    return render_template("dashboard.html", suggestions=suggestions, performance_data=performance_data)

@users_bp.route('/profile/view')
@login_required
def view_profile():
    return render_template('view_profile.html', user=current_user)