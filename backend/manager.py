from flask_migrate import Migrate
from app import create_app, db

app = create_app()

migrate = Migrate(app, db)

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    # 使用 Migrate 对象来初始化数据库
    migrate.init_app(app, db)
    return app

if __name__ == "__main__":
    app.run(host="localhost", port=11451)
