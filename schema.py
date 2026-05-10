from sqlalchemy import inspect, text

from database import db


def ensure_schema():
    inspector = inspect(db.engine)
    bill_columns = {column["name"] for column in inspector.get_columns("bill")}

    if "currency" not in bill_columns:
        db.session.execute(text("ALTER TABLE bill ADD COLUMN currency VARCHAR(3) NOT NULL DEFAULT 'USD'"))
        db.session.commit()

    if "category" not in bill_columns:
        db.session.execute(text("ALTER TABLE bill ADD COLUMN category VARCHAR(30) NOT NULL DEFAULT 'other'"))
        db.session.commit()
