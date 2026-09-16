from database.db import db


class EmergencyContact(db.Model):

    __tablename__ = "emergency_contacts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "emergency_contacts",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<EmergencyContact {self.name}>"