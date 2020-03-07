import requests

from linkdump import db
from linkdump.models import Item


def create_item(user, url):
    response = requests.head(url)
    if not response.ok:
        return False, None

    (created, item) = Item.create(source=url, process=True)
    item: Item
    if created:
        print('item %s created' % item)
    else:
        print('using item %s from db' % item)
    if item not in user.items.all():
        user.add_item(item)
    else:
        print('user already has this item')
    db.session.commit()
    return True, item
