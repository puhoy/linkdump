from linkdump import db
from datetime import datetime

class Bookmarks(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column('id', db.Integer, primary_key=True)

    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column('item_id', db.Integer, db.ForeignKey('items.id'))

    user = db.relationship('Item', backref=db.backref("bookmarks", cascade="all, delete-orphan" ))
    item = db.relationship('User', backref=db.backref("bookmarks", cascade="all, delete-orphan" ))

    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<bookmark %s - %s>' % (self.user, self.item)
