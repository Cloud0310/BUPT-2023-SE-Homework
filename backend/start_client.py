from flask.cli import FlaskGroup
from app.scheduler import scheduler
import asyncio

from app import create_app

app = create_app()
cli = FlaskGroup(app)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler.run_scheduler())
    cli()
