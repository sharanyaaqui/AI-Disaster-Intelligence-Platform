from flask import Flask
import os

from config import Config
from database.db import db

# Import Models
from models.user import User
from models.report import Report

# Import Routes
from routes.auth import auth
from routes.reports import reports

# Create Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Create uploads folder automatically if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize database
db.init_app(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(reports)

# Create database tables
with app.app_context():
    db.create_all()

# Home Route
@app.route("/")
def home():
    return {
        "status": "Backend Running",
        "project": "AI Disaster Intelligence Platform"
    }
print(app.url_map)
# Run the application
if __name__ == "__main__":
    app.run(debug=True)