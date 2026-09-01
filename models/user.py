from database.db import db


class User(db.Model):
    reports = db.relationship(
    "Report",
    backref="user",
    lazy=True
)
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    preferred_language = db.Column(
        db.String(5),
        default="en",
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="citizen",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<User {self.email}>"