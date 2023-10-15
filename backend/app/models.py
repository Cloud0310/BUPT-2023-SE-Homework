from app import app
from flask_sqlalchemy import SQLAlchemy

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buptse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库实例
db = SQLAlchemy(app)

# 定义模型类
class Record(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    room = db.Column(db.String(50))

    def __init__(self, id, room):
        self.id = id
        self.room = room

    def save(self):
        db.session.add(self)
        db.session.commit()