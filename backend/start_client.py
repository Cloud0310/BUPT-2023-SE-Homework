from flask.cli import FlaskGroup
from app.scheduler import scheduler
from app import create_app
import asyncio

bupt_se_app = create_app()
bupt_vpl_app = create_app()
bupt_se_client = FlaskGroup(bupt_se_app)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(scheduler.run_scheduler())
    # loop.run_forever()
    loop.create_task(scheduler.run_scheduler())
    bupt_se_client()