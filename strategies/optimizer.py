def simple_ai_recommendation(current_holdings, live_prices):
    recommendations = []

    for holding in current_holdings:
        symbol = holding["symbol"]
        quantity = holding["quantity"]
        purchase_price = holding["purchase_price"]
        current_price = live_prices.get(symbol)

        if current_price:
            try:
                current_price = float(current_price)
                purchase_price = float(purchase_price)
                profit_percent = (current_price - purchase_price) / purchase_price * 100

                if profit_percent > 10:
                    recommendations.append(f"Sell 10% of {symbol}")
                elif profit_percent < -5:
                    recommendations.append(f"Buy 15% more of {symbol}")
                else:
                    recommendations.append(f"Hold {symbol}")
            except ValueError:
                recommendations.append(f"Unable to analyze {symbol} due to invalid price data.")

    return recommendations
