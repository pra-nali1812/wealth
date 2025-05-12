import numpy as np

class PortfolioRLAgent:
    def __init__(self, n_assets, n_steps=1000, alpha=0.01, gamma=0.95):
        self.n_assets = n_assets
        self.n_steps = n_steps
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.weights = np.ones(n_assets) / n_assets  # equal allocation

    def act(self):
        noise = np.random.randn(self.n_assets) * 0.01
        action = self.weights + noise
        action = np.clip(action, 0, 1)
        action /= np.sum(action)  # normalize
        return action

    def train(self, price_matrix):
        n_days = price_matrix.shape[0]
        for step in range(self.n_steps):
            t = np.random.randint(0, n_days - 2)
            current_prices = price_matrix[t]
            next_prices = price_matrix[t + 1]

            action = self.act()
            portfolio_return = np.dot(next_prices / current_prices, action) - 1

            self.weights += self.alpha * portfolio_return * action
            self.weights = np.clip(self.weights, 0, 1)
            self.weights /= np.sum(self.weights)

        return self.weights
