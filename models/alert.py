from database.db import db
from datetime import datetime


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    message = db.Column(db.Text, nullable=False)

    disaster_type = db.Column(db.String(50))

    location = db.Column(db.String(100))

    severity = db.Column(db.String(20))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )