from database.db import db
from models.alert import Alert


def create_alert(
    title,
    message,
    disaster_type,
    location,
    severity
):

    alert = Alert(
        title=title,
        message=message,
        disaster_type=disaster_type,
        location=location,
        severity=severity
    )

    db.session.add(alert)
    db.session.commit()

    return alert


def get_all_alerts():
    return Alert.query.order_by(
        Alert.created_at.desc()
    ).all()