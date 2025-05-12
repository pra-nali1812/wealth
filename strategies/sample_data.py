import numpy as np

def generate_dummy_price_data(n_assets=3, n_days=100):
    np.random.seed(42)
    prices = np.cumprod(1 + 0.001 * np.random.randn(n_days, n_assets), axis=0) * 100
    return prices
