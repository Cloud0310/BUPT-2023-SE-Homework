from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建 SQLAlchemy 实例
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 导入配置
    app.config.from_object("app.config.Config")

    # 初始化扩展
    db.init_app(app)

    # 注册蓝图
    from app.views.auth import auth_blueprint

    # from app.views.data import data_blueprint
    from app.views.query import query_blueprint
    from app.views.room import room_blueprint
    from app.views.admin import admin_blueprint
    from app.views.control import control_blueprint

    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(data_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(room_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(control_blueprint)

    return app
