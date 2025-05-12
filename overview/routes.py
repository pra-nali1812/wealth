from flask import Blueprint, render_template, request, send_file
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding
from strategies.ai_model import recommend_portfolio
from performance.utils import generate_line_chart  # Assumes this returns image path
from extensions import db

import io
import matplotlib.pyplot as plt

overview_bp = Blueprint('overview', __name__)

@overview_bp.route('/overview')
def overview():
    user_id = request.args.get("user_id", type=int, default=1)

    # Query all user assets
    stocks = StockHolding.query.filter_by(user_id=user_id).all()
    cryptos = CryptoHolding.query.filter_by(user_id=user_id).all()
    mutuals = MutualFundHolding.query.filter_by(user_id=user_id).all()

    # Total value and breakdown
    total_value = 0
    asset_breakdown = {"Stocks": 0, "Crypto": 0, "Mutual Funds": 0}

    for s in stocks:
        asset_breakdown["Stocks"] += s.quantity * s.purchase_price
    for c in cryptos:
        asset_breakdown["Crypto"] += c.quantity * c.purchase_price
    for m in mutuals:
        asset_breakdown["Mutual Funds"] += m.quantity * m.purchase_price

    total_value = sum(asset_breakdown.values())

    # Mock ROI and P/L — replace with actual logic later
    roi = round((total_value - 10000) / 10000 * 100, 2)  # Assume 10k invested
    profit_loss = round(total_value - 10000, 2)

    # AI recommendation
    ai_suggestion = recommend_portfolio(user_id)

    return render_template(
        "overview.html",
        total_value=total_value,
        roi=roi,
        profit_loss=profit_loss,
        asset_breakdown=asset_breakdown,
        ai_suggestion=ai_suggestion,
    )
@overview_bp.route('/overview/chart')
def performance_chart():
    user_id = request.args.get("user_id", type=int, default=1)
    fig = generate_line_chart(user_id)

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype='image/png')
