from application import db
from application.models import Base
from sqlalchemy import event
from sqlalchemy.sql import text


class User(Base):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        if(self.is_admin):
            return ["ADMIN"]
        else:
            return []

    @staticmethod
    def find_users_with_most_features():
        stmt = text("SELECT Account.id, Account.username, COUNT(*) AS feature_count FROM Feature"
                    " LEFT JOIN Account ON Account.id = Feature.user_id"
                    " GROUP BY Feature.user_id"
                    " ORDER BY feature_count DESC"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({
                "id": row[0],
                "username": row[1],
                "feature_count": row[2]
            })
        return response


def init_users(*args, **kwargs):
    db.session.add(User("admin", "pass", True))
    db.session.commit()


event.listen(User.__table__, 'after_create', init_users)
