from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required=True,
        help = "This field cannot be left blank!"
    )
    # now instead of:
    #   data = request.get_json()
    # we can say:
    #   data = parser.parse_args()
    parser.add_argument('store_id',
        type = int,
        required=True,
        help = "Every item needs a store id."
    )

    @jwt_required()

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404



#checks if an item already exists:
    def post(self, name):

        # we can call this       if Item.find_by_name(name)    as well
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400


        # #checks if an item already exists:
        # if next(filter(lambda x: x['name'] == name, items), None):
        #     return {'message': "An item with name '{}' already exists".format(name)}, 400

        # needing from flask import request
        # Force = True will format the content/type header even if not set
        # data = request.get_json(force = True)

        # silent = True will just give None
        # data = request.get_json(silent = True)

        data = Item.parser.parse_args()

        #data = request.get_json()


        item = ItemModel(name, **data) # '**data' is   data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        #cannot return item objects, but only json
        return item.json(), 201




    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}


    def put(self, name):
        data = Item.parser.parse_args()      #parsing the args coming through the json
            # payload and put the valid ones in data

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()



class ItemList(Resource):
    # haven't passed any params in Postman, so not having here as well:
    def get(self):

        # can also do:    return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': [x.json() for x in ItemModel.query.all()]}
