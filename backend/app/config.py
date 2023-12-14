import os

class Config:
    # Config server address and port
    FLASK_RUN_HOST = "0.0.0.0"
    FLASK_RUN_PORT = 11451

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("data/Bupt.db")
    SECRET_KEY = 'ILOVEBUPT'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
