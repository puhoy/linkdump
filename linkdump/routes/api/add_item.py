from linkdump import app
from linkdump.models import User


@app.route()
def add_item():
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return ''
    url = request.json['url']
    response = requests.head(url)
    if not response.ok:
        return 'cant access %s' % url

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
    return 'added %s' % url, 200