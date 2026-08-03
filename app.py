from flask import Flask
from config import Config
from database.db import db

# Import Models
from models.user import User
from models.report import Report

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Connect SQLAlchemy to Flask
db.init_app(app)

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

if __name__ == "__main__":
    app.run(debug=True)