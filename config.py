import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://wm:password@localhost/wm_db' )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

