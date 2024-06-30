from datetime import datetime
import random
from . import db

# Associação muitos-para-muitos entre Record e Tag
record_tag = db.Table(
    "record_tag",
    db.Column("record_id", db.Integer, db.ForeignKey("record.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


def generate_random_color_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    records = db.relationship("Record", backref="user", lazy=True)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tags = db.relationship(
        "Tag",
        secondary=record_tag,
        lazy="subquery",
        backref=db.backref("records", lazy=True),
    )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color_hex = db.Column(
        db.String(7), default=generate_random_color_hex, nullable=False
    )
