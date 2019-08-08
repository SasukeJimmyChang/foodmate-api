from flask import Flask
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from instance.config import Config

from datetime import datetime

db = SQLAlchemy()

from foodmate.model.user import User as UserModel
from foodmate.resource.user import User, UserList
from instance.config import app_config

def create_app(config_name = "development"):

    flask_app = Flask(__name__, instance_relative_config=True)
    app = Api(app = flask_app, version="1.0", prefix="/v1", title="Foodmate-API", description="foodmate api")

    flask_app.config.from_object(app_config[config_name])
    db.init_app(flask_app)
    migrate = Migrate(flask_app,db)

    us = app.namespace('user', description='Manage users')
    us.add_resource(UserList, "/all", methods = ["GET"])
    us.add_resource(User, "/<int:id>", methods = ["GET", "PUT"])
    us.add_resource(User, "/create", methods = ["POST"])
    
    # api.add_resource(User, "/auth/login", methods = ["POST"])
    # api.add_resource(EventList, "/events")
    # api.add_resource(Event, "/event/<int:id>", methods = ["GET", "PUT"])

    return flask_app