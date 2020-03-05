from datetime import date, datetime

import requests
from readability import Document

from linkdump import db, dramatiq
from xml.etree import ElementTree


class Item(db.Model):
    __tablename__ = 'items'

    __table_args__ = (
        db.UniqueConstraint('source', 'date_added',
                            name='_source_at_date'),
    )

    id = db.Column(db.Integer, primary_key=True)

    source = db.Column(db.String, nullable=False)

    date_added = db.Column(db.Date, nullable=False,
                           default=date.today)

    title = db.Column(db.String(250), nullable=True)
    body = db.Column(db.Text, nullable=True)

    date_processing_started = db.Column(db.DateTime, nullable=True)
    date_processing_finished = db.Column(db.DateTime, nullable=True)

    users = db.relationship("User", secondary="bookmarks", lazy='dynamic')

    @property
    def body_plain_text(self):
        return ''.join(ElementTree.fromstring(self.body).itertext())

    @staticmethod
    def create(source, title=None, body=None, date_added=None, save=True, process=True) -> (bool, 'Item'):
        if not date_added:
            date_added = date.today()

        item = Item.query.filter_by(source=source, date_added=date_added).first()
        created = False
        if not item:
            item = Item()
            created = True

            item.source = source
            item.title = title
            item.body = body
            if date_added:
                item.date_added = date_added

            if save:
                db.session.add(item)
                db.session.commit()
            
            if save and process:
                item.process()
            
        return created, item

    def __repr__(self):
        return '<Item %s finished@%s>' % (self.id, self.date_processing_finished)

    def process(self):
        print('processing item...')
        _process_url.send(self.id, self.source)


@dramatiq.actor(max_retries=3)
def _process_url(id: int, url: str):
    date_processing_started = datetime.utcnow()
    response = requests.get(url)
    doc = Document(response.text)
    title = doc.title()
    body = doc.summary(html_partial=True)
    date_processing_finished = datetime.utcnow()

    item = Item.query.get(id)
    item.date_processing_started = date_processing_started
    item.date_processing_finished = date_processing_finished
    item.title = title
    item.body = body

    db.session.add(item)
    db.session.commit()
