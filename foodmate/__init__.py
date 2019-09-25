# 引用必要套件
from flask import Flask
import firebase_admin
from firebase_admin import credentials, auth, firestore, initialize_app
from flask_restplus import Api, Resource
from firebase_admin import auth
import pyrebase


# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
Cred = credentials.Certificate("service-account-file.json")
# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(Cred)
# 初始化firestore
firebaseDb = firestore.client()

from foodmate.resource.user import UserList, User, SendEmail

from instance.config import app_config

def create_app(config_name = "development"):

    flask_app = Flask(__name__, instance_relative_config = True)
    flask_app.config.from_object(app_config[config_name])
    firebase = pyrebase.initialize_app(app_config[config_name].config)

    api = Api(app = flask_app, version="1.0", prefix="/v1", title="Foodmate-API", description="foodmate api")

    us = api.namespace('user', description='Manage users')

    us.add_resource(UserList, "/all_users", methods = ["GET"])
    us.add_resource(User, "/<string:uid>", methods = ["GET", "PUT", "DELETE"])
    us.add_resource(User, "/create", methods = ["POST"])
    # us.add_resource(SendEmail, "/forgotPassword", methods = ["POST"])

    return flask_app