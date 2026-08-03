from database.db import db
from datetime import datetime

class Report(db.Model):

    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    disaster_type = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text)

    image_path = db.Column(db.String(255))

    prediction = db.Column(db.String(100))

    confidence = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)