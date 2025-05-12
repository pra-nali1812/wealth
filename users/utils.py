from flask_login import login_user, logout_user

def login_current_user(user):
    login_user(user)

def logout_current_user():
    logout_user()