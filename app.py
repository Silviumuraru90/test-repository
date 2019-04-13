import os                   # to have access to the environment variables

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
# now loking into the 'resources' package and then finding the file:
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# Important to leave 'sqlite:///data.db' as well - to leave this path for local testing
# locally will use the second value if the seond one is not to be found.


# the following turns of the flask_sqlalchemy modification tracker
# it does not turn of the SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)     # creates /auth endpoint

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')      # /item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')


# On import we dont want to run things, as if we import a class from app.py into
# a different file then app.run will get run

# THIS PREVENTS the above from happening:
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

# Explanation is that the file that's run is assigned __main__ as a __name__
# So, if we run another file that will be __main__ and if in that file we
# import app.py, app.py will not be main anymore, so the condition won't be met
