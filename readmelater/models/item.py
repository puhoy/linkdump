from readmelater import db
from datetime import datetime


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)

    source = db.Column(db.String, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)

    date_added = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User',
                           backref=db.backref('items', lazy=True))
