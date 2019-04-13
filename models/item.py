# importing the 'db' variable from the 'db' file
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))    # precision is the nr of decimals

    # stores.id     --> table's name and then column's name
    # ForeignKey is a relationship between item's stored id and the store's id, so
    # you cannot delete the store as long as there are items with the store's id
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}


    @classmethod
    def find_by_name(cls, name):
        # 'query' now is not smth we've defined, but somth coming from SQLAlchemy
        # so it's the same as    SELECT * FROM items WHERE name=name
        # we can also do   return ItemModel.query.filter_by(name=name).filter_by(id=1)
        # or               return ItemModel.query.filter_by(name=name, id=1)
        # so:    SELECT * FROM items WHERE name=name LIMIT 1
        # this will return an ItemModel obj. having self.name and self.price
        return ItemModel.query.filter_by(name=name).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
