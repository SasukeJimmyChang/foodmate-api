from foodmate import db


class Base(db.Model):

    __abstract__ = True

    def add(self):
        # 新增
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # 刪除
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        # 更新
        db.session.commit()

    def as_dict(self):
        # 转字典
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}