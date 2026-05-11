# app.py
from flask import Flask
from flask_cors import CORS

from auth_routes import auth_bp
from bill_routes import bills_bp
from config import Config
from database import db
from schedule_routes import schedule_bp
from schema import ensure_schema

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://127.0.0.1:8000",
            "http://localhost:8000",
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "http://127.0.0.1:5501",
            "http://localhost:5501",
            "http://127.0.0.1:5502",
            "http://localhost:5502",
            "null",
        ],
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(bills_bp)
    app.register_blueprint(schedule_bp)

    with app.app_context():
        db.create_all()
        ensure_schema()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
