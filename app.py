from flask import Flask, render_template, send_from_directory
import os
from flask_cors import CORS

from config import Config
from database.db import db

# Import Models
from models.user import User
from models.report import Report
from models.alert import Alert

# Import Routes
from routes.auth import auth
from routes.reports import reports
from routes.alerts import alerts
from routes.chatbot import chatbot as chatbot_blueprint


# Create Flask app
app = Flask(__name__)

CORS(app)

# Load configuration
app.config.from_object(Config)

# Create uploads folder automatically if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize database
db.init_app(app)

# Register backend blueprints
app.register_blueprint(auth)
app.register_blueprint(reports)
app.register_blueprint(alerts)
app.register_blueprint(chatbot_blueprint)


# Create database tables
with app.app_context():
    db.create_all()


# =========================
# FRONTEND PAGE ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/report")
def report_page():
    return render_template("report.html")


@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")


@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")


@app.route("/offline")
def offline():
    return render_template("offline.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


# =========================
# UPLOADED FILES
# =========================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)