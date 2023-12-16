from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# 创建 SQLAlchemy 实例
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Import config
    app.config.from_object("app.config.Config")
    app.config["HOST"] = "0.0.0.0"
    app.config["PORT"] = 11451

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.views.auth import auth_blueprint
    from app.views.query import query_blueprint
    from app.views.room import room_blueprint
    from app.views.admin import admin_blueprint
    from app.views.control import control_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(room_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(control_blueprint)

    # Test
    from app.views import hello_blueprint
    app.register_blueprint(hello_blueprint)

    return app
