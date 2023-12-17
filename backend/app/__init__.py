from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

"""
Hint: __init__.py is a special file that is run when the app is initialized.
"""

# Create app instance
def create_app():
    # Initialize app
    app = Flask(__name__)
    CORS(app, origins="*", supports_credentials=True)

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
    from app.views.client import client_blueprint

    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(room_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(control_blueprint)
    app.register_blueprint(client_blueprint)

    return app

# Create SQLAlchemy instance
db = SQLAlchemy()
migrate = Migrate()