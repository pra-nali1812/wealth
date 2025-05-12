from market_data.utils import get_stock_price, get_crypto_price, get_fund_price

def fetch_current_prices(user):
    prices = {}

    for stock in user.stocks:
        data = get_stock_price(stock.stock_symbol)
        prices[stock.stock_symbol] = float(data.get("05. price", 0))

    for crypto in user.cryptos:
        data = get_crypto_price(crypto.crypto_symbol)
        prices[crypto.crypto_symbol] = float(data.get("5. Exchange Rate", 0))

    for fund in user.mutual_funds:
        data = get_fund_price(fund.fund_symbol)
        prices[fund.fund_symbol] = float(data.get("price", 0))

    return prices
