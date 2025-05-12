from flask import request, jsonify
from . import strategies_bp
from .ai_model import generate_recommendations
from users.models import User
from portfolio.models import StockHolding, CryptoHolding, MutualFundHolding
from extensions import db

@strategies_bp.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    actions = generate_recommendations(user)
    return jsonify({'actions': actions})
from flask import Blueprint, render_template, request
from .ai_model import recommend_portfolio

strategies_bp = Blueprint('strategies', __name__)

@strategies_bp.route('/recommend/view')
def recommend_view():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return "User ID is required", 400

    recommendations = recommend_portfolio(user_id)
    return render_template('recommendation.html', recommendations=recommendations)
from flask import Blueprint, jsonify, request, render_template
from .ai_model import recommend_portfolio

strategies_bp = Blueprint('strategies', __name__)

@strategies_bp.route('/recommend/view')
def view_recommendation():
    user_id = request.args.get("user_id", type=int, default=1)
    recommendations = recommend_portfolio(user_id)
    return render_template("recommendation.html", recommendations=recommendations)
