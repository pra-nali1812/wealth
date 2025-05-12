def init_app(app):
    from .routes import market_data_bp
    app.register_blueprint(market_data_bp, url_prefix="/api/market")
