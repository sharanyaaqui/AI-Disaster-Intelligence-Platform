from database.db import db
from models.report import Report


def create_report(user_id, disaster_type, description, latitude, longitude, image=None):

    report = Report(
        user_id=user_id,
        disaster_type=disaster_type,
        description=description,
        latitude=latitude,
        longitude=longitude,
        image=image
    )

    db.session.add(report)
    db.session.commit()

    return report


def get_all_reports():
    return Report.query.order_by(Report.created_at.desc()).all()


def get_report_by_id(report_id):
    return Report.query.get(report_id)


def verify_report(report_id, status):

    report = Report.query.get(report_id)

    if not report:
        return None

    report.status = status

    db.session.commit()

    return report