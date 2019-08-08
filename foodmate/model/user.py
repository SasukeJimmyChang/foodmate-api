from foodmate import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from foodmate.model.base import Base

class User(Base):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    gender = db.Column(db.String(2)) # 0 = 未選擇, 1 = Male, 2 = Female
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    job_title = db.Column(db.String(64))
    info = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "id={}, username={}, password_hash={}".format(
            self.id, self.username, self.password_hash
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_by_name(username):
        return db.session.query(User).filter(
            User.username == username
        ).first()
    
    @staticmethod
    def get_by_id(id):
        return db.session.query(User).filter(
            User.id == id
        ).first()

    @staticmethod
    def get_user_list():
        return db.session.query(User).all()

    @staticmethod
    def authenticate(username, password):
        user_find = db.session.query(User).filter(
            User.username == username
        ).first()
        print(user_find)
        if user_find:
            # check password
            if user_find.check_password(password):
                return user_find

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        user = User.get_by_id(user_id)
        return user