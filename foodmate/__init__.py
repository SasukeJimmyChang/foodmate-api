# 引用必要套件
from flask import Flask
import firebase_admin
from firebase_admin import credentials, auth, firestore, initialize_app
from flask_restplus import Api, Resource
from firebase_admin import auth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pyrebase

from datetime import datetime

# 初始化 DB
db = SQLAlchemy()

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
Cred = credentials.Certificate("instance/service-account-file.json")
# 初始化 firebase，注意不能重複初始化
firebase_admin.initialize_app(Cred)
# 初始化 firestore
firebaseDb = firestore.client()

from instance.config import app_config

# 初始化 pyrebase
firebase = pyrebase.initialize_app(app_config["development"].Config)

from foodmate.resource.user import UserList, User, Auth, SendEmail

def create_app(config_name = "development"):

    flask_app = Flask(__name__, instance_relative_config = True)
    flask_app.config.from_object(app_config[config_name])

    db.init_app(flask_app)
    migrate = Migrate(flask_app,db)

    api = Api(app = flask_app, version="1.0", prefix="/v1", title="Foodmate-API", description="foodmate api")
    # Authentication API
    authNamespace = api.namespace("auth", description = "Authentication")
    authNamespace.add_resource(Auth, "/login", methods = ["POST"])
    # Manage users API
    userNamespace = api.namespace("user", description = "Manage users")
    userNamespace.add_resource(UserList, "/all_users", methods = ["GET"])
    userNamespace.add_resource(User, "/<string:uid>", methods = ["PUT", "DELETE"])
    userNamespace.add_resource(User, "/create", methods = ["POST"])
    userNamespace.add_resource(SendEmail, "/forgotPassword", methods = ["POST"])
    userNamespace.add_resource(User, "/<string:id_token>", methods = ["GET"])

    return flask_app