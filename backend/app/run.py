from flask_cors import CORS
from app import create_app
from app.scheduler import scheduler

"""
Hint: run.py is a file that is run when the app is started.
"""

if __name__ == "__main__":
    app = create_app()
    scheduler.run_scheduler(app.app_context())
    app.run(host="0.0.0.0", port=11451)
