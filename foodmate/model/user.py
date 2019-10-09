from foodmate import db
from datetime import datetime, timedelta
from flask import current_app
from foodmate.model.base import Base

class User(Base):
    localId = db.Column(db.Integer, primary_key = True) #uid
    email = db.Column(db.String(64), unique=True) #account
    displayName = db.Column(db.String(64)) #暱稱
    gender = db.Column(db.String(2)) # 0 = 未選擇, 1 = Male, 2 = Female
    job_title = db.Column(db.String(24))
    idToken = db.Column(db.String(1000))
    refreshToken = db.Column(db.String(1000))
    registered = db.Column(db.Boolean)
    expiresIn = db.Column(db.String(10))
    info = db.Column(db.String(256))

    def __repr__(self):
        return "localId={}, email={}, idToken={}".format(
            self.localId, self.email, self.idToken
        )