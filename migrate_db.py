from app import app
from database.db import db
from sqlalchemy import inspect, text

with app.app_context():

    inspector = inspect(db.engine)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "vulnerabilities" not in columns:

        with db.engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN vulnerabilities TEXT NOT NULL DEFAULT '[]'"
                )
            )

        print("vulnerabilities column added successfully.")

    else:
        print("vulnerabilities column already exists.")

    print("Database migration completed.")