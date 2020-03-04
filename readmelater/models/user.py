from readmelater import db
from readmelater.models.item import Item
from readmelater.models import Bookmarks


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    items = db.relationship("Item", secondary="bookmarks", lazy='dynamic')
    
    def add_item(self, item: 'Item'):
        bookmark = Bookmarks()
        bookmark.item = item
        bookmark.user = self
        self.items.append(bookmark)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def create(username, email, save=True):
        user = User()
        user.username = username
        user.email = email

        if save:
            db.session.add(user)
            db.session.commit()
        return user

    def add_item(self, item: Item, save=True):
        self.items.append(item)

        if save:
            db.session.add(item)
            db.session.commit()
