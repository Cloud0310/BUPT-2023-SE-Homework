from app import create_app
from flask_cors import CORS
from flask.cli import FlaskGroup

if __name__ == "__main__":
    app = create_app()
    CORS(app)
    cli = FlaskGroup(app)
    app.run(host="0.0.0.0", port=11451)
