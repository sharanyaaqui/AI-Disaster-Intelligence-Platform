from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.translation_service import translate
from database.db import db
from models.user import User

# Create Blueprint
auth = Blueprint("auth", __name__)


# -------------------------
# Register API
# -------------------------
@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    language = data.get("language", "en")

    # Check required fields
    if not full_name or not email or not password:
        return jsonify({
            "success": False,
            "message": translate("required_fields", language)
        }), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": translate("email_exists", language)
        }), 409

    # Hash password
    hashed_password = generate_password_hash(password)

    # Create new user
    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        preferred_language=language,
        role="citizen"
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": translate("user_registered", language),
        "user": {
            "name": full_name,
            "language": language
        }
    }), 201


# -------------------------
# Login API
# -------------------------
@auth.route("/login", methods=["POST"])
def login():

    # Default language
    language = "en"

    # Get request data
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Check required fields
    if not email or not password:
        return jsonify({
            "success": False,
            "message": translate("login_required", language)
        }), 400

    # Find user
    user = User.query.filter_by(email=email).first()

    # If user exists, use their preferred language
    if user:
        language = user.preferred_language

    # User not found
    if not user:
        return jsonify({
            "success": False,
            "message": translate("user_not_found", language)
        }), 404

    # Check password
    if not check_password_hash(user.password, password):
        return jsonify({
            "success": False,
            "message": translate("invalid_password", language)
        }), 401

    # Login successful
    return jsonify({
        "success": True,
        "message": translate("login_success", language),
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "language": user.preferred_language,
            "role": user.role
        }
    }), 200
