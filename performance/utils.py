def calculate_roi(purchase_price, current_price):
    try:
        purchase_price = float(purchase_price)
        current_price = float(current_price)
    except ValueError:
        return 0  # or raise an error if that fits your use case better

    if purchase_price == 0:
        return 0

    return (current_price - purchase_price) / purchase_price * 100


import matplotlib.pyplot as plt
import random

def generate_line_chart(user_id):
    # Mock data: 12 months of value
    months = [f'M{i+1}' for i in range(12)]
    values = [10000 + random.uniform(-1000, 2000) for _ in range(12)]

    fig, ax = plt.subplots()
    ax.plot(months, values, marker='o')
    ax.set_title("Portfolio Performance")
    ax.set_ylabel("Value ($)")
    ax.set_xlabel("Month")
    ax.grid(True)
    return fig
