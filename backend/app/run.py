from app import create_app
from app.controller import scheduler

def main():
    app = create_app()
    with app.app_context():
        scheduler.run_scheduler()
    app.run(host="0.0.0.0", port=11451, debug=False)

if __name__ == "__main__":
    main()
