import asyncio
from flask.cli import FlaskGroup
from app import create_app
from app.controller import scheduler

# 创建 Flask 应用程序
app = create_app()

# 创建 Flask CLI 组
cli = FlaskGroup(app)


if __name__ == "__main__":
    # 获取事件循环
    loop = asyncio.get_event_loop()

    # 创建任务并运行调度器
    scheduler_task = loop.create_task(scheduler.run_scheduler())

    # 启动 Flask CLI
    cli()
