from flask import Blueprint, request, jsonify

from services.alert_service import (
    create_alert,
    get_all_alerts
)

alerts = Blueprint("alerts", __name__)


@alerts.route("/alerts", methods=["GET"])
def get_alerts():

    alert_list = get_all_alerts()

    data = []

    for alert in alert_list:

        data.append({
            "id": alert.id,
            "title": alert.title,
            "message": alert.message,
            "disaster_type": alert.disaster_type,
            "location": alert.location,
            "severity": alert.severity,
            "created_at": alert.created_at
        })

    return jsonify({
        "success": True,
        "alerts": data
    })


@alerts.route("/alerts", methods=["POST"])
def add_alert():

    data = request.get_json()

    alert = create_alert(
        data.get("title"),
        data.get("message"),
        data.get("disaster_type"),
        data.get("location"),
        data.get("severity")
    )

    return jsonify({
        "success": True,
        "message": "Alert created",
        "id": alert.id
    }), 201