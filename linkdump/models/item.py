from datetime import date, datetime
import re

import requests
from readability import Document
from sqlalchemy import Index, or_, and_

from linkdump import db, dramatiq
from xml.etree import ElementTree

from linkdump.models import User


class Item(db.Model):
    __tablename__ = 'items'

    __table_args__ = (
        db.UniqueConstraint('source', 'date_added',
                            name='_source_at_date'),
    )

    id = db.Column(db.Integer, primary_key=True)

    source = db.Column(db.String, nullable=False)
    source_response_raw = db.Column(db.Text, nullable=True)

    date_added = db.Column(db.Date, nullable=False,
                           default=date.today)

    title = db.Column(db.String(250), nullable=True)
    body = db.Column(db.Text, nullable=True)
    body_plain_text = db.Column(db.Text, nullable=True)

    date_processing_started = db.Column(db.DateTime, nullable=True)
    date_processing_finished = db.Column(db.DateTime, nullable=True)

    users = db.relationship("User", secondary="bookmarks", lazy='dynamic')

    @staticmethod
    def strip_tags(html):
        return ''.join(ElementTree.fromstring(html).itertext())

    @staticmethod
    def create(source, html=None, date_added=None) -> (bool, 'Item'):
        if not date_added:
            date_added = date.today()

        item = Item.query.filter_by(source=source, date_added=date_added).first()
        created = False
        if not item:
            item = Item()
            created = True

            item.source = source
            if date_added:
                item.date_added = date_added

            if html:
                date_processing_started = datetime.utcnow()
                item.populate_from_html(html)
                date_processing_finished = datetime.utcnow()
                item.date_processing_started = date_processing_started
                item.date_processing_finished = date_processing_finished

            db.session.add(item)
            db.session.commit()

            if not html:
                item.process()

        return created, item

    def __repr__(self):
        return '<Item %s finished@%s>' % (self.id, self.date_processing_finished)

    def process(self):
        print('processing item...')
        _process_url.send(self.id, self.source)

    def text_around_word(self, word, n):
        index = self.body_plain_text.find(word)
        prefix = ''
        suffix = ''

        if index == -1:
            return ''

        if index - n < 0:
            start = 0
        else:
            start = index - n
            prefix = '...'
        if index + len(word) + n >= len(self.body_plain_text):
            end = len(self.body_plain_text) - 1
        else:
            end = index + len(word) + n
            suffix = '...'
        return prefix + self.body_plain_text[start:end] + suffix

    def populate_from_html(self, html):

        doc = Document(html)

        title = doc.title()
        body = doc.summary(html_partial=True)
        body_plain_text = Item.strip_tags(body)

        self.source_response_raw = html
        self.title = title
        self.body = body
        self.body_plain_text = body_plain_text

    @classmethod
    def search(cls, query_string, user=None):
        filters = []
        for term in query_string.split(' '):
            filters.append(
                or_(cls.title.ilike('%{}%'.format(term)),
                    cls.source.ilike('%{}%'.format(term)),
                    cls.body_plain_text.ilike('%{}%'.format(term))
                    )
            )
        query = cls.query
        if user:
            query = query.filter(Item.users.any(User.id == user.id))
        items = query.filter(
            and_(*filters)
        ).distinct()
        return items


item_source_index = Index('item_source_idx', Item.source)
item_title_index = Index('item_title_idx', Item.source)
item_body_plain_text_index = Index('item_body_plain_text_idx', Item.source)


@dramatiq.actor(max_retries=3)
def _process_url(id: int, url: str):
    date_processing_started = datetime.utcnow()
    response = requests.get(url)

    date_processing_finished = datetime.utcnow()

    item = Item.query.get(id)

    item.populate_from_html(response.text)

    item.date_processing_started = date_processing_started
    item.date_processing_finished = date_processing_finished

    db.session.add(item)
    db.session.commit()
