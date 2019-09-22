from foodmate import app, firebaseDb
from flask_restplus import Resource, reqparse, api
from firebase_admin import auth

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


class UserList(Resource):

    def get(self):
        """
        取得用戶列表
        """
        user_list = auth.list_users().iterate_all()
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

class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "phone_number", type = min_length_str(10)
    )
    parser.add_argument(
        "password", type = min_length_str(8)
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

    def get(self, uid):   #/user/uid
        """
        2.5 Get Member Detail
        """
        find_user = auth.get_user(uid)
        type(find_user)
        return {
            "user":{
                "uid":find_user.uid,
                "phone_number":find_user.phone_number,
                "display_name":find_user.display_name,
                "photo_url":find_user.photo_url,
                "disabled":find_user.disabled
            }
        }
    
    def post(self):   # POST /user/create
        """
        1.4 Register
        """
        data = User.parser.parse_args()
        print(data)
        newUser = auth.create_user(
        phone_number = data["phone_number"],
        display_name = data["display_name"]
        )
        return {
            "message":"create suscced",
            "user":{
                "uid":newUser.uid,
                "phone_number":newUser.phone_number
            }
        }, 201
    
    def put(self, uid):  # PUT /user/uid
        """
        2.3 Update Member Information
        """
        find_user = auth.get_user(uid)
        if find_user:
            data = User.parser.parse_args()
            print(data)
            userUpdate = auth.update_user(
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