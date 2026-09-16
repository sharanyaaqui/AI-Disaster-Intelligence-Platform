from flask import Flask, render_template, send_from_directory, session, redirect, url_for, request, Response
import os
import json
from flask_cors import CORS
from utils.translation_service import translate


from config import Config
from database.db import db

# Import Models
from models.user import User
from models.report import Report
from models.alert import Alert
from models.emergency_contact import EmergencyContact

# Import Routes
from routes.auth import auth
from routes.reports import reports
from routes.alerts import alerts
from routes.chatbot import chatbot as chatbot_blueprint


# Create Flask app
app = Flask(__name__)
@app.context_processor
def inject_translation():
    language = session.get("language", "en")

    return {
        "t": lambda key: translate(key, language)
    }

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


@app.route("/profile", methods=["GET", "POST"])
def profile():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login_page"))

    user = User.query.get(user_id)

    if not user:
        return redirect(url_for("login_page"))

    if request.method == "POST":

        user.full_name = request.form.get("full_name")
        user.email = request.form.get("email")
        user.preferred_language = request.form.get(
            "language",
            "en"
        )
        session["language"] = user.preferred_language

        db.session.commit()

        return redirect(url_for("profile"))

    # Load saved vulnerabilities
    vulnerabilities = json.loads(
        user.vulnerabilities or "[]"
    )

    return render_template(
        "profile.html",
        user=user,
        vulnerabilities=vulnerabilities
    )

@app.route("/profile/emergency-contact", methods=["POST"])
def add_emergency_contact():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login_page"))

    name = request.form.get("emergency_contact_name")
    phone = request.form.get("emergency_contact_phone")

    if not name or not phone:
        return redirect(url_for("profile"))

    contact = EmergencyContact(
        user_id=user_id,
        name=name,
        phone=phone
    )

    db.session.add(contact)
    db.session.commit()

    return redirect(url_for("profile"))

@app.route("/profile/emergency-contact/delete/<int:contact_id>")
def delete_emergency_contact(contact_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login_page"))

    contact = EmergencyContact.query.filter_by(
        id=contact_id,
        user_id=user_id
    ).first()

    if contact:
        db.session.delete(contact)
        db.session.commit()

    return redirect(url_for("profile"))

@app.route("/profile/vulnerabilities", methods=["POST"])
def update_vulnerabilities():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login_page"))

    user = User.query.get(user_id)

    if not user:
        return redirect(url_for("login_page"))

    selected_vulnerabilities = request.form.getlist("vulnerability")

    user.vulnerabilities = json.dumps(
        selected_vulnerabilities
    )

    db.session.commit()

    return redirect(url_for("profile"))


# =========================
# UPLOADED FILES
# =========================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(
        app.static_folder,
        "js/service-worker.js",
        mimetype="application/javascript"
    )

@app.route("/maps/<path:filename>")
def serve_map(filename):
    file_path = os.path.join(app.static_folder, "maps", filename)

    if not os.path.exists(file_path):
        return "Map file not found", 404

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range")

    if not range_header:
        return send_from_directory(
            os.path.join(app.static_folder, "maps"),
            filename
        )

    byte_range = range_header.replace("bytes=", "").split("-")
    start = int(byte_range[0])

    if byte_range[1]:
        end = int(byte_range[1])
    else:
        end = file_size - 1

    end = min(end, file_size - 1)

    length = end - start + 1

    with open(file_path, "rb") as f:
        f.seek(start)
        data = f.read(length)

    response = Response(
        data,
        206,
        mimetype="application/octet-stream",
        direct_passthrough=True
    )

    response.headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Content-Length"] = str(length)

    return response

# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        ssl_context=("certs/divya-cert.pem", "certs/divya-key.pem")
    )