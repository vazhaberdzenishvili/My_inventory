import os

APP_NAME = "MyInventory"

# SQLAlchemy CONFIG
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
# FLASK-USER CFG
USER_APP_NAME = APP_NAME


# Flask-User settings
class Config(object):
    USER_APP_NAME = APP_NAME
    USER_ENABLE_EMAIL = True  # Register with Email
    USER_ENABLE_USERNAME = True  # Register and Login with username
    USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password

    USER_ENABLE_CONFIRM_EMAIL = False  # Force users to confirm their email
    USER_ENABLE_FORGOT_PASSWORD = False  # Allow users to reset their passwords

    USER_ENABLE_REGISTRATION = True  # Allow new users to register
    USER_ENABLE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:

    USER_AFTER_LOGIN_ENDPOINT = 'StoreModel.Store'
    USER_AFTER_LOGOUT_ENDPOINT = 'main.home_page'
    # oauth configuration
    # GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    # GITHUB_OAUTH_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
    # GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    # GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    GITHUB_OAUTH_CLIENT_ID = 'e4bfdbbc8ee6e9925b5d'
    GITHUB_OAUTH_CLIENT_SECRET = '735eca90efa45409b1fb649c9a0bf653b0713575'
    GOOGLE_OAUTH_CLIENT_ID = '625406787313-uo5b44n1tt03h9c1fib68ngmo3mo527o.apps.googleusercontent.com'
    GOOGLE_OAUTH_CLIENT_SECRET = 'j7ONuaIeRYEZIgC4Z2UxSldS'

    # flask-babel configuration
    LANGUAGES = {
        "en": "English",
        "ka": "Georgian"
    }
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DOMAIN = 'messages'
