from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename

from models.user import User
from services.report_service import (
    create_report,
    get_all_reports,
    get_report_by_id,
    verify_report,
    total_reports,
    pending_reports,
    verified_reports,
    rejected_reports,
    get_reports_by_type,
    get_reports_by_status,
    get_recent_reports
)


reports = Blueprint("reports", __name__)


# =====================================================
# POST /report
# Submit Disaster Report
# =====================================================
@reports.route("/report", methods=["POST"])
def report_disaster():

    data = request.get_json()

    user_id = data.get("user_id")
    disaster_type = data.get("disaster_type")
    description = data.get("description")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    image = data.get("image")

    if not all([user_id, disaster_type, description, latitude, longitude]):
        return jsonify({
            "success": False,
            "message": "Missing required fields"
        }), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    report = create_report(
        user_id,
        disaster_type,
        description,
        latitude,
        longitude,
        image
    )

    return jsonify({
        "success": True,
        "message": "Report submitted successfully",
        "report": {
            "id": report.id,
            "disaster_type": report.disaster_type,
            "status": report.status,
            "language": user.preferred_language
        }
    }), 201


# =====================================================
# GET /reports
# =====================================================
@reports.route("/reports", methods=["GET"])
def get_reports():

    reports_list = get_all_reports()

    data = []

    for report in reports_list:
        data.append({
            "id": report.id,
            "disaster_type": report.disaster_type,
            "description": report.description,
            "location": {
                "latitude": report.latitude,
                "longitude": report.longitude
            },
            "image": report.image,
            "status": report.status,
            "reported_by": report.user.full_name,
            "created_at": report.created_at
        })

    return jsonify({
        "success": True,
        "total_reports": len(data),
        "reports": data
    }), 200


# =====================================================
# GET /report/<id>
# =====================================================
@reports.route("/report/<int:report_id>", methods=["GET"])
def get_single_report(report_id):

    report = get_report_by_id(report_id)

    if not report:
        return jsonify({
            "success": False,
            "message": "Report not found"
        }), 404

    return jsonify({
        "success": True,
        "report": {
            "id": report.id,
            "user_id": report.user_id,
            "disaster_type": report.disaster_type,
            "description": report.description,
            "location": {
                "latitude": report.latitude,
                "longitude": report.longitude
            },
            "image": report.image,
            "status": report.status,
            "reported_by": report.user.full_name,
            "created_at": report.created_at
        }
    }), 200


# =====================================================
# PUT /report/<id>/verify
# =====================================================
@reports.route("/report/<int:report_id>/verify", methods=["PUT"])
def verify_disaster_report(report_id):

    data = request.get_json()

    status = data.get("status")

    if status not in ["Pending", "Verified", "Rejected"]:
        return jsonify({
            "success": False,
            "message": "Invalid status"
        }), 400

    report = verify_report(report_id, status)

    if not report:
        return jsonify({
            "success": False,
            "message": "Report not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Report updated successfully",
        "report": {
            "id": report.id,
            "status": report.status
        }
    }), 200


# =====================================================
# POST /report/image
# =====================================================
@reports.route("/report/image", methods=["POST"])
def upload_image():

    print(request.files)

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image uploaded"
        }), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    filename = secure_filename(image.filename)

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(filepath)

    return jsonify({
        "success": True,
        "message": "Image uploaded successfully",
        "filename": filename
    }), 201
    # =====================================================
# GET /dashboard
# Dashboard Statistics
# =====================================================
@reports.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({
        "success": True,
        "statistics": {
            "total_reports": total_reports(),
            "pending_reports": pending_reports(),
            "verified_reports": verified_reports(),
            "rejected_reports": rejected_reports()
        }
    }), 200
    # =====================================================
# GET /reports/type/<disaster_type>
# Filter Reports by Disaster Type
# =====================================================
@reports.route("/reports/type/<string:disaster_type>", methods=["GET"])
def reports_by_type(disaster_type):

    reports_list = get_reports_by_type(disaster_type)

    data = []

    for report in reports_list:
        data.append({
            "id": report.id,
            "disaster_type": report.disaster_type,
            "description": report.description,
            "status": report.status,
            "reported_by": report.user.full_name,
            "created_at": report.created_at
        })

    return jsonify({
        "success": True,
        "total_reports": len(data),
        "reports": data
    }), 200
    # =====================================================
# GET /reports/status/<status>
# =====================================================
@reports.route("/reports/status/<string:status>", methods=["GET"])
def reports_by_status(status):

    reports_list = get_reports_by_status(status)

    data = []

    for report in reports_list:
        data.append({
            "id": report.id,
            "disaster_type": report.disaster_type,
            "description": report.description,
            "status": report.status,
            "reported_by": report.user.full_name,
            "created_at": report.created_at
        })

    return jsonify({
        "success": True,
        "total_reports": len(data),
        "reports": data
    }), 200
    # =====================================================
# GET /reports/recent
# =====================================================
@reports.route("/reports/recent", methods=["GET"])
def recent_reports():

    reports_list = get_recent_reports()

    data = []

    for report in reports_list:
        data.append({
            "id": report.id,
            "disaster_type": report.disaster_type,
            "description": report.description,
            "status": report.status,
            "reported_by": report.user.full_name,
            "created_at": report.created_at
        })

    return jsonify({
        "success": True,
        "reports": data
    }), 200