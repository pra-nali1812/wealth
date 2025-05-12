from dotenv import load_dotenv
from flask import Flask
from config import Config
from extensions import db, login_manager,migrate
from users.routes import users_bp
from portfolio.routes import portfolio_bp
from market_data import init_app
from strategies.routes import strategies_bp
from performance.routes import performance_bp
from overview.routes import overview_bp
import os
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
init_app(app)
# Init extensions
db.init_app(app)
migrate.init_app(app, db)

login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(users_bp)
app.register_blueprint(portfolio_bp)

app.register_blueprint(overview_bp)
app.register_blueprint(strategies_bp, url_prefix="/strategies")
app.register_blueprint(performance_bp, url_prefix='/performance')


if __name__ == '__main__':
    app.run(debug=True)