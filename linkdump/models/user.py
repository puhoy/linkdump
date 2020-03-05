from flask_security import UserMixin

from linkdump import db
from linkdump.models.item import Item
from linkdump.models import Bookmarks

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(80))
    current_login_ip = db.Column(db.String(80))
    login_count = db.Column(db.Integer)

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
