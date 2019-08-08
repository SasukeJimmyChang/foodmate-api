from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from instance.config import Config

from datetime import datetime

db = SQLAlchemy()

from foodmate.model.user import User as UserModel
from foodmate.resource.user import User, UserList
from instance.config import app_config

def create_app(config_name = "development"):

    app = Flask(__name__)
    api = Api(app, prefix="/v1", title="Foodmate-API", description="foodmate api")
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    migrate = Migrate(app,db)

    # api.add_resource(User, "/auth/login", methods = ["POST"])
    api.add_resource(UserList, "/users")
    api.add_resource(User, "/user/<int:id>", methods = ["GET", "PUT"])
    api.add_resource(User, "/user", methods = ["POST"])
    # api.add_resource(EventList, "/events")
    # api.add_resource(Event, "/event/<int:id>", methods = ["GET", "PUT"])

    return app