import os

class Config:
    # 服务器地址和端口配置
    FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    FLASK_RUN_PORT = int(os.environ.get("FLASK_RUN_PORT", 11451))

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("data/Bupt.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24).hex())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
