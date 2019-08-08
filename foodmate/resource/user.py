from foodmate import db, app
from foodmate.model.user import User as UserModel
from flask_restplus import Resource, reqparse, api
from datetime import datetime


def min_length_str(min_length):
    def validate(s):
        if s is None:
            raise Exception('password required')
        if not isinstance(s, (int, str)):
            raise Exception('password format error')
        s = str(s)
        if len(s) >= min_length:
            return s
        raise Exception("String must be at least %i characters long" % min_length)
    return validate


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=min_length_str(9), required=True
    )
    parser.add_argument(
        'password', type=min_length_str(8), required=True
    )
    parser.add_argument(
        'email', type=str, required=True
    )

    def get(self, id):
        """
        取讀用戶資料
        """
        find_user = UserModel.get_by_id(id)
        print(find_user)
        if find_user:
            if isinstance(find_user.create_time, datetime):
                find_user.create_time = find_user.create_time.isoformat()
            if isinstance(find_user.id, int):
                find_user.id = str(find_user.id)
            return {"user":find_user.as_dict()}
        return {'message': 'user not found'}, 404

    def post(self):   # POST /user
        """
        建立用戶
        """
        data = User.parser.parse_args()
        print(data)
        find_user = UserModel.get_by_name(data["username"])
        if find_user:
            return {"message": "user already exist"}
        new_user = UserModel(
            username = data["username"],
            email = data["email"],
            gender = "0",
        )
        new_user.set_password(data["password"])
        print(new_user)
        UserModel.add(new_user)
        return {
            "message":"create suscced"
        }, 201

    def put(self, id):
        """
        更新用戶
        """
        find_user = UserModel.get_by_id(id)
        print(find_user)
        if find_user:
            data = User.parser.parse_args()
            find_user.username = data["username"]
            find_user.email = data["email"]
            find_user.set_password(data["password"])
            find_user.update()
            # datetime 轉 string
            if isinstance(find_user.create_time, datetime):
                find_user.create_time = find_user.create_time.isoformat()
            # int 轉 string
            if isinstance(find_user.id, int):
                find_user.id = str(find_user.id)
            return find_user.as_dict()
        else:
            return {'message': "user not found"}, 204    


class UserList(Resource):

    def get(self):
        """
        取得用戶列表
        """
        user_list = UserModel.get_user_list()
        print(user_list)
        if user_list:
            for user in user_list:
                if isinstance(user.id, int):
                    user.id = str(user.id)
                if isinstance(user.create_time, datetime):
                    user.create_time = str(user.create_time)
            return {
                "users": [u.as_dict() for u in user_list]
                    }