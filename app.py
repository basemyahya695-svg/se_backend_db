from flask import Flask
from flask_cors import CORS

# Import Configuration and Database
from config import Config
from database import db
from schema import ensure_schema

# Import Blueprints (Routes)
from auth_routes import auth_bp
from bill_routes import bills_bp
from schedule_routes import schedule_bp

# Initialize the Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS (Allows your frontend HTML/JS to communicate with this backend)
# supports_credentials=True is MANDATORY for session-based login to work
CORS(app, supports_credentials=True)

# Link the Database to the App
db.init_app(app)

# Register the routes from the other files
app.register_blueprint(auth_bp)
app.register_blueprint(bills_bp)
app.register_blueprint(schedule_bp)

# Run the Application
if __name__ == "__main__":
    # Create the database tables if they don't exist yet
    with app.app_context():
        db.create_all()
        ensure_schema()
        
    app.run(debug=True, port=5000)
