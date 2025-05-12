from flask import Blueprint, request, jsonify, render_template
from .utils import get_stock_price, get_crypto_price
from .utils import get_fund_price
market_data_bp = Blueprint("market_data", __name__)

@market_data_bp.route("/stock", methods=["GET"])
def stock_price():
    symbol = request.args.get("symbol", "AAPL")
    data = get_stock_price(symbol)
    return jsonify(data)

@market_data_bp.route("/crypto", methods=["GET"])
def crypto_price():
    symbol = request.args.get("symbol", "BTC")
    market = request.args.get("market", "USD")
    data = get_crypto_price(symbol, market)
    return jsonify(data)


@market_data_bp.route("/fund", methods=["GET"])
def fund_price():
    symbol = request.args.get("symbol", "VTSAX")
    data = get_fund_price(symbol)
    return jsonify(data)




