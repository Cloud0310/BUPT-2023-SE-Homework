## backend 目录结构简介

```
backend/
    app/
        static/         # 静态文件
        templates/      # 模板文件
        __init__.py     # 初始化
        app.py          # 原神启动！
        models.py       # 数据库模型
        views.py        # 视图函数
    migrations/         # 数据库迁移文件
    test/               # 测试文件
    config.py           # 配置文件
```

> 另外，`buptse.db` 和 `buptse.sql` 是测试用的数据库文件，目前无作用