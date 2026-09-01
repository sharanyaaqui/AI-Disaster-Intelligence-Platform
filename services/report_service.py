from database.db import db
from models.report import Report


# =====================================================
# Create a Disaster Report
# =====================================================
def create_report(
    user_id,
    disaster_type,
    description,
    latitude,
    longitude,
    image=None
):

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


# =====================================================
# Get All Reports
# =====================================================
def get_all_reports():

    return Report.query.order_by(
        Report.created_at.desc()
    ).all()


# =====================================================
# Get Single Report by ID
# =====================================================
def get_report_by_id(report_id):

    return Report.query.get(report_id)


# =====================================================
# Verify / Reject Report
# =====================================================
def verify_report(report_id, status):

    report = Report.query.get(report_id)

    if not report:
        return None

    report.status = status

    db.session.commit()

    return report


# =====================================================
# Dashboard Statistics
# =====================================================
def total_reports():
    return Report.query.count()


def pending_reports():
    return Report.query.filter_by(status="Pending").count()


def verified_reports():
    return Report.query.filter_by(status="Verified").count()


def rejected_reports():
    return Report.query.filter_by(status="Rejected").count()
    # =====================================================
# Filter Reports by Disaster Type
# =====================================================
def get_reports_by_type(disaster_type):

    return Report.query.filter_by(
        disaster_type=disaster_type
    ).all()
    # =====================================================
# Get Reports by Status
# =====================================================
def get_reports_by_status(status):

    return Report.query.filter_by(
        status=status
    ).all()
    # =====================================================
# Get Recent Reports
# =====================================================
def get_recent_reports(limit=5):

    return Report.query.order_by(
        Report.created_at.desc()
    ).limit(limit).all()