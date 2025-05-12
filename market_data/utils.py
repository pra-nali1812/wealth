import requests
import yfinance as yf
from datetime import datetime, timedelta
from .alpha_vantage_config import ALPHA_VANTAGE_API_KEY, BASE_URL

# --- Cache for mutual fund prices ---
fund_cache = {}

def get_stock_price(symbol):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data.get("Global Quote", {})

def get_crypto_price(symbol="BTC", market="USD"):
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": symbol,
        "to_currency": market,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data.get("Realtime Currency Exchange Rate", {})

def get_fund_price(symbol):
    now = datetime.now()

    # Use cached price if recent (within 5 minutes)
    if symbol in fund_cache:
        cached_price, timestamp = fund_cache[symbol]
        if now - timestamp < timedelta(minutes=5):
            return {"symbol": symbol, "price": round(cached_price, 2)}

    try:
        fund = yf.Ticker(symbol)
        todays_data = fund.history(period='1d')
        if not todays_data.empty:
            price = todays_data['Close'].iloc[-1]
            fund_cache[symbol] = (price, now)
            return {"symbol": symbol, "price": round(price, 2)}
        else:
            print(f"No data for symbol: {symbol}")
            return {"symbol": symbol, "price": "No data available"}
    except Exception as e:
        print(f"Error fetching mutual fund price: {e}")
        return {"symbol": symbol, "price": "Error"}
