import os

"""
Hint: config.py is a file that contains all the configuration variables for the app.
"""

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

class Config:
    # Config server address and port
    FLASK_RUN_HOST = "0.0.0.0"
    FLASK_RUN_PORT = 11451
    # Config database
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("data/Bupt.db")
    SECRET_KEY = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
