from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 创建 SQLAlchemy 实例
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # 配置
    configure_app(app)

    # 初始化扩展
    initialize_extensions(app)

    # 注册蓝图
    register_blueprints(app)

    return app


def configure_app(app):
    # 添加CORS支持
    CORS(app, origins="*", supports_credentials=True)

    # 导入配置
    app.config.from_object("app.config.Config")

    # 修改 host 和 port
    app.config["HOST"] = "0.0.0.0"
    app.config["PORT"] = 11451


def initialize_extensions(app):
    # 初始化数据库扩展
    db.init_app(app)

    # 初始化迁移扩展
    migrate.init_app(app, db)


def register_blueprints(app):
    # 导入蓝图
    from app.views.auth import auth_blueprint
    from app.views.query import query_blueprint
    from app.views.room import room_blueprint
    from app.views.admin import admin_blueprint
    from app.views.control import control_blueprint
    from app.views.client import client_blueprint

    # 注册蓝图
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(room_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(control_blueprint)
    app.register_blueprint(client_blueprint)


if __name__ == "__main__":
    app = create_app()
    app.run()
