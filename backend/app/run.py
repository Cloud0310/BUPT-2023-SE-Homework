from app import create_app
from app.scheduler import scheduler

if __name__ == "__main__":
    app = create_app()
    scheduler.run_scheduler(app.app_context())
    app.run(host="0.0.0.0", port=11451, debug=False)
