from foodmate import app, firebaseDb, firebase
from flask_restplus import Resource, reqparse, fields, marshal_with
from firebase_admin import auth as adminAuth
import requests, urllib3
from requests.exceptions import HTTPError
from instance.config import app_config
import firebase_admin

pyAuth = firebase.auth()

def min_length_str(min_length):
    def validate(s):
        if s is None:
            raise Exception("input required")
        if not isinstance(s, (int, str)):
            raise Exception("format error")
        s = str(s)
        if len(s) >= min_length:
            return s
        raise Exception("String must be at least %i characters long" % min_length)
    return validate

class userModel(object):
    {
    "email": fields.String,
    "password": fields.String
    }
    

class Auth(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type = str, required = True 
    )
    parser.add_argument(
        "password", type = str, required = True
    )


    @marshal_with(userModel)
    def post(self):  # 1.1 POST /auth/login
        """
        User Login
        """
        try:
            jsonData = Auth.parser.parse_args()
            print(jsonData)
            userLogin = pyAuth.sign_in_with_email_and_password(jsonData["email"], jsonData["password"])
            return {
                "message":"login succssed",
                "userUid":userLogin
            }
        except requests.exceptions.HTTPError:
            return {
                "message":"OOPS! Somthing Wrong~~"
            }

class UserList(Resource):

    def get(self):
        """
        Get all users
        """
        user_list = adminAuth.list_users().iterate_all()
        print (user_list)
        if user_list:
            count = 0
            user_no = []
            user_uid = []
            for user in user_list:
                count += 1
                print("user"+str(count)+":"+user.uid)
                user_no.append("user"+str(count))
                user_uid.append(user_uid)
            return {
                "message":"success"
            }

class SendEmail(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type = str
    )
    def post(self):   # 1.3 POST /user/forgotPassword
        """
        Forgot Password
        """
        try:
            data = SendEmail.parser.parse_args()
            print(data)
            pyAuth.send_password_reset_email(data["email"])
            return {
                "message":"email: The email of the user whose password is to be reset."
                }
        except adminAuth.exceptions.InvalidArgumentError:
            return {
                "message":"Error while calling adminAuth service (MISSING_EMAIL):"
            }

class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "phone_number", type = min_length_str(10)
    )
    parser.add_argument(
        "password", type = min_length_str(8)
    )
    parser.add_argument(
        "re_password", type = min_length_str(8)
    )
    parser.add_argument(
        "email", type = str
    )
    parser.add_argument(
        "display_name", type = min_length_str(3)
    )
    parser.add_argument(
        "photo_url"
    )
    parser.add_argument(
        "disabled", type = bool
    )
    parser.add_argument(
        "id_token", type = str
    )

    def post(self):   # 1.4 POST /user/create
        """
        Register
        """
        jsonData = User.parser.parse_args()
        print(jsonData)
        if jsonData["password"] == jsonData["re_password"]:
            try:
                newUser = adminAuth.create_user(
                    email = jsonData["email"],
                    password = jsonData["password"],
                    phone_number = jsonData["phone_number"]
                    )
                print(newUser)
                return {
                    "message":"create suscced",
                    "user":
                    {
                    "uid":newUser.uid,
                    "phone_number":newUser.phone_number,
                    "email":newUser.email
                    }
                    },201
            except adminAuth.PhoneNumberAlreadyExistsError:
                    return {
                        "message":"Phone Number Already Exists"
                    }
            except firebase_admin.exceptions.InvalidArgumentError as err:
                print(err)
                return {
                    "message":err.__str__()
                }
        else:
            return {
                "message":"Password Is Different, Plz Try Again"
            }

    
    def delete(self,uid):   # 1.5 delete /user/delete
        """
        Delete Account
        """
        try:
            adminAuth.delete_user(uid)
            return {
                "message":"Delete Successed"}
        except adminAuth.UserNotFoundError:
            return {
                    "message":"User Not Found",
                }

    
    def put(self, uid):  # 2.3 PUT /user/uid
        """
        Update Member Information
        """
        try :
            find_user = adminAuth.get_user(uid)
            if find_user:
                data = User.parser.parse_args()
                print(data)
                userUpdate = adminAuth.update_user(
                    find_user.uid,
                    phone_number = data["phone_number"],
                    display_name = data["display_name"],
                    photo_url = data["photo_url"],
                    disabled = data["disabled"]
                )
                return {
                    "message":"Sucessfully updated user",
                    "user":{
                        "uid":userUpdate.uid,
                        "display_name":userUpdate.display_name,
                        "photo_url":userUpdate.photo_url,
                        "disabled":userUpdate.disabled
                    }
                }
            else:
                return {"message": "user not found"}, 204
        except adminAuth.UserNotFoundError:
            return {
                    "message":"User Not Found",
                }

    def get(self, id_token):   #2.5 /user/uid
        """
        Get Member Detail
        """
        # jsonData = User.parser.parse_args()
        print(id_token)
        try:
            find_user = pyAuth.get_account_info(id_token)
            type(find_user)
            return {
                "message":"Susscced",
                "userInfo":find_user
            }
        except requests.exceptions.HTTPError:
            return {
                    "message":"INVALID_ID_TOKEN",
                }