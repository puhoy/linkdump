from readmelater import db

user_item_association_table = db.Table('user_item_association',
                                       db.Column('user_id',
                                                 db.Integer,
                                                 db.ForeignKey('users.id'),
                                                 ),
                                       db.Column('item_id',
                                                 db.Integer,
                                                 db.ForeignKey('items.id'))
                                       )
